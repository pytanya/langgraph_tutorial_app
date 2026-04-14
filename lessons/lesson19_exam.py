import streamlit as st
import random
import requests
import os
import json
import re
import math
import logging

# Настройка логирования в файл
logging.basicConfig(
    filename='exam_generation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger("RAG_Exam")

# Попытка импортировать Torch и SentenceTransformers для локальной проверки
try:
    import torch
    from sentence_transformers import CrossEncoder
    HAS_LOCAL_EVAL = True
except ImportError:
    HAS_LOCAL_EVAL = False

# ==========================================
# 1. Загрузка Кросс-энкодера
# ==========================================
@st.cache_resource(show_spinner="Загрузка локального реранкера (Оценщика)...")
def load_evaluator():
    if not HAS_LOCAL_EVAL: return None
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return CrossEncoder("DiTy/cross-encoder-russian-msmarco", device=device, max_length=512)

# ==========================================
# 2. Динамическая База Знаний (Парсинг уроков)
# ==========================================
@st.cache_data(show_spinner="Сбор конспектов из всех уроков Академии...")
def build_knowledge_base():
    import glob
    knowledge = []
    lessons_dir = os.path.dirname(__file__)
    for file_path in glob.glob(os.path.join(lessons_dir, "lesson*.py")):
        if "lesson19" in file_path or "lesson20" in file_path: continue
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r'st\.markdown\(\s*["\']{3}(.*?)["\']{3}', content, re.DOTALL)
            for m in matches:
                clean_text = m.strip()
                if len(clean_text) > 80: knowledge.append(clean_text)
    if not knowledge: knowledge = ["LangGraph использует StateGraph для маршрутизации агентов и MemorySaver для долгосрочной памяти."]
    return list(set(knowledge))

KNOWLEDGE_BASE = build_knowledge_base()

# ==========================================
# 3. API Генераторы (Одиночный вопрос и JSON)
# ==========================================
def generate_question_via_openrouter(api_key: str, context: str, model_name: str) -> str:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Ты - строгий преподаватель по программированию. Прочитай контекст RAG и задай ОДИН сложный проверочный вопрос студенту. Только вопрос без ответов."},
            {"role": "user", "content": f"ТЕКСТ ИЗ УРОКА:\n{context}"}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            st.error(f"Ошибка API: {response.text}")
            return "Не удалось сгенерировать вопрос."
    except requests.exceptions.SSLError:
        st.error("🚫 Ошибка SSL: Соединение сброшено. Попробуйте сменить VPN.")
        return "Ошибка сети."
    except Exception as e:
        st.error(f"🚨 Сетевая ошибка: {str(e)}")
        return "Не удалось связаться с сервером."

def generate_json_test(api_key, context, model_name, num_q=3):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system = """Ты составляешь тест по программированию по предоставленному материалу. Верни СТРОГО JSON массив.
Формат КАЖДОГО вопроса (ВСЕ поля обязательны):
{"question": "текст вопроса?", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "почему этот ответ верный"}
Правила:
- correct: число от 0 до 3 (индекс правильного ответа)
- ВЕРНИ ТОЛЬКО JSON МАССИВ. Никакого текста до или после!
- КРИТИЧЕСКИ ВАЖНО: Не используй двойные кавычки (") внутри самих текстов вопросов и ответов, заменяй их на одинарные (')!"""
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Контекст:\n{context}\n\nСоздай {num_q} вопросов. ВЕРНИ ТОЛЬКО РАБОЧИЙ JSON МАССИВ."}
        ],
        "temperature": 0.2
    }
    
    logger.info(f"=== Старт генерации теста. Модель: {model_name}, Вопросов: {num_q} ===")
    for attempt in range(3):
        try:
            logger.info(f"Попытка #{attempt + 1}...")
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                logger.info(f"Ответ получен ({len(result)} символов).")
                
                result_clean = re.sub(r'^```json\s*|\s*```$', '', result.strip(), flags=re.MULTILINE)
                
                # Ищем первый '[' и последний ']' во всем ответе
                start_idx = result_clean.find('[')
                end_idx = result_clean.rfind(']')
                
                if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                    json_str = result_clean[start_idx:end_idx+1]
                    try:
                        valid_json = json.loads(json_str)
                        logger.info("✅ JSON успешно распарсен и валидирован!")
                        return valid_json
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Ошибка JSONDecodeError: {e}\nСырой JSON:\n{json_str}")
                else:
                    logger.error(f"❌ В ответе не найдена структура массива: {result[:200]}")
            else:
                logger.error(f"❌ HTTP Ошибка {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"❌ Сбой сети или непредвиденная ошибка: {e}")
            
    st.error("🚨 Не удалось сгенерировать правильный JSON за 3 попытки (см. логи в exam_generation.log).")
    return []

# ==========================================
# 4. Динамический загрузчик моделей
# ==========================================
@st.cache_data(show_spinner="Загрузка списка бесплатных моделей...")
def get_free_openrouter_models():
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", [])
            # Ищем модели, где в ID есть "free" или цена = 0
            free_models = [
                m["id"] for m in data 
                if ":free" in m["id"].lower() or 
                (m.get("pricing") and float(m["pricing"].get("prompt", 1) or 1) == 0.0)
            ]
            if free_models:
                # Добавим для уверенности те модели, что уже знаем, если их там не оказалось
                default_known = ["liquid/lfm-40b:free", "z-ai/glm-4.5-air:free", "google/gemma-2-9b-it:free"]
                return sorted(list(set(free_models + default_known)))
    except Exception as e:
        logger.error(f"Не удалось загрузить список моделей: {e}")
        
    return ["liquid/lfm-40b:free", "z-ai/glm-4.5-air:free", "google/gemma-2-9b-it:free"]

# ==========================================
# 5. Основной UI
# ==========================================
def render():
    st.header("Урок 19: Интерактивный RAG-Экзамен")
    
    if not HAS_LOCAL_EVAL:
        st.error("⚠️ Для локальной оценки установите библиотеки: `pip install torch sentence-transformers`")
        return
        
    evaluator = load_evaluator()
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
        
    env_key = os.getenv("OPENROUTER_API_KEY", "")
    default_model_env = os.getenv("OPENROUTER_DEFAULT_MODEL", "liquid/lfm-40b:free")
    
    if env_key:
        api_key = env_key
        st.success("✅ Ключ безопасности автоматически считан из системного окружения (.env).")
    else:
        api_key = st.text_input("🔑 Введите ваш OpenRouter API Key", type="password")
    
    free_models_list = get_free_openrouter_models()
    
    # Если default_model_env (значение из .env) не в списке, мы всё равно добавим его
    if default_model_env not in free_models_list:
        free_models_list.insert(0, default_model_env)
        
    # Определяем какой индекс выбрать по умолчанию
    try:
        default_idx = free_models_list.index(default_model_env)
    except ValueError:
        default_idx = 0
        
    model_name = st.selectbox(
        "🤖 Выберите модель (OpenRouter)", 
        options=free_models_list, 
        index=default_idx,
        help="Список бесплатных моделей загружается динамически с OpenRouter API."
    )
    
    # ---------------- ВЫБОР РЕЖИМА ----------------
    st.markdown("### Выбор режима")
    mode = st.radio("В каком формате проводить экзамен?", [
        "💬 Свободный ответ (Кросс-Энкодер проверяет смысл)", 
        "📝 Тест с вариантами ответов (Автогенерация ответов LLM)"
    ])
    st.divider()
    
    # ---------------- РЕЖИМ 1 ----------------
    if mode == "💬 Свободный ответ (Кросс-Энкодер проверяет смысл)":
        if "exam_context" not in st.session_state: st.session_state.exam_context = ""
        if "exam_question" not in st.session_state: st.session_state.exam_question = ""

        if st.button("🎲 Сгенерировать новый вопрос", type="primary"):
            if not api_key:
                st.warning("Введите API ключ.")
                return
            with st.spinner("LLM придумывает вопрос по случайному конспекту..."):
                st.session_state.exam_context = random.choice(KNOWLEDGE_BASE)
                st.session_state.exam_question = generate_question_via_openrouter(api_key, st.session_state.exam_context, model_name)
                if "student_answer" in st.session_state: st.session_state.student_answer = ""
                    
        if st.session_state.exam_question:
            st.info(f"**Вопрос преподавателя:**\n\n{st.session_state.exam_question}")
            user_answer = st.text_area("Ваш ответ:", key="student_answer")
            
            if st.button("✅ Проверить ответ локально"):
                if not user_answer.strip():
                    st.warning("Напишите ответ!")
                    return
                with st.spinner("Локальная ИИ проверяет ответ..."):
                    score = evaluator.predict([[user_answer, st.session_state.exam_context]])
                    score_val = float(score) if not hasattr(score, '__len__') else float(score[0])
                    try:
                        prob = 1 / (1 + math.exp(-score_val))
                    except OverflowError:
                        prob = 0.0 if score_val < 0 else 1.0
                    
                    st.markdown("### Результат автопроверки:")
                    st.caption(f"🔍 Оценщик: `DiTy/cross-encoder-russian-msmarco` | Raw Logit: `{score_val:.4f}`")
                    if prob > 0.4:
                        st.success(f"🎉 Правильно! Вы поняли суть. (Сходство смысла: {prob*100:.1f}%)")
                    else:
                        st.error(f"❌ Смысл ответа не совпадает или ответ слишком короткий. (Сходство: {prob*100:.1f}%)")
                        st.markdown(f"**Оригинальный текст:**\n_{st.session_state.exam_context}_")
                        
    # ---------------- РЕЖИМ 2 ----------------
    elif mode == "📝 Тест с вариантами ответов (Автогенерация ответов LLM)":
        if "quiz_data" not in st.session_state: st.session_state.quiz_data = None
        num_questions = st.slider("Количество вопросов в тесте:", min_value=1, max_value=10, value=3)
        
        if st.button("🚀 Сгенерировать полноценный Тест", type="primary"):
            if not api_key:
                st.warning("Введите API ключ.")
                return
            with st.spinner(f"Создаю тест из {num_questions} вопросов... Это может занять около минуты."):
                # Объединяем абзацы из курса пропорционально количеству вопросов для богатого контекста
                ctx = "\n".join(random.sample(KNOWLEDGE_BASE, min(num_questions + 1, len(KNOWLEDGE_BASE))))
                st.session_state.quiz_data = generate_json_test(api_key, ctx, model_name, num_q=num_questions)
                
        data = st.session_state.quiz_data
        if data:
            st.success("✅ Тест успешно сгенерирован!")
            with st.form("quiz_form"):
                user_selections = []
                for i, q in enumerate(data):
                    st.markdown(f"**Вопрос {i+1}:** {q.get('question')}")
                    choice = st.radio("Выберите ответ:", q.get('options', []), key=f"q_{i}", label_visibility="collapsed")
                    user_selections.append(choice)
                    st.markdown("---")
                
                if st.form_submit_button("Отправить на проверку"):
                    score = 0
                    st.subheader("Результаты:")
                    for i, q in enumerate(data):
                        opts = q.get('options', [])
                        correct_idx = q.get('correct', 0)
                        correct_ans = opts[correct_idx] if correct_idx < len(opts) else opts[0]
                        
                        if user_selections[i] == correct_ans:
                            st.success(f"✅ Вопрос {i+1}: Верно! ({correct_ans})")
                            score += 1
                        else:
                            st.error(f"❌ Вопрос {i+1}: Ошибка! Вы выбрали '{user_selections[i]}'")
                            st.info(f"👉 Правильный ответ: **{correct_ans}**\n\n💡 Пояснение: _{q.get('explanation', '')}_")
                    st.metric("Итоговый балл:", f"{score} / {len(data)}")
