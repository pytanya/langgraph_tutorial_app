import streamlit as st
import random
import requests

# Попытка импортировать Torch и SentenceTransformers для локальной проверки
try:
    import torch
    from sentence_transformers import CrossEncoder
    HAS_LOCAL_EVAL = True
except ImportError:
    HAS_LOCAL_EVAL = False

# ==========================================
# 1. Загрузка Кросс-энкодера (Кэшируется)
# ==========================================
@st.cache_resource(show_spinner="Загрузка локального реранкера (Оценщика)...")
def load_evaluator():
    if not HAS_LOCAL_EVAL: return None
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Легковесная модель для русского языка (~90mb), чтобы оценивать текст локально
    return CrossEncoder("DiTy/cross-encoder-russian-msmarco", device=device, max_length=512)

# ==========================================
# 2. RAG База знаний (Выдержки из курса)
# ==========================================
KNOWLEDGE_BASE = [
    "StateGraph — это основной объект в LangGraph. Он инкапсулирует состояние (State) и маршрутизацию между изолированными узлами (Nodes).",
    "Алгоритм Pregel использует барьеры синхронизации. Это позволяет LangGraph выполнять независимые узлы параллельно внутри одного супер-шага.",
    "Functional API идеален для жестких и линейных пайплайнов без циклов. Если вам нужен Агент с зацикливанием для самокоррекции, используйте классический StateGraph.",
    "MemorySaver позволяет сохранять промежуточную историю треда (thread_id). Это дает агентам отказоустойчивость (Durable Execution) и позволяет возвращаться в прошлое (Time Travel).",
    "Нельзя хранить строковые промпты (текст) внутри State агента. State должен содержать только сырые атомарные данные (словари), а форматирование промпта нужно делать внутри самого узла перед вызовом LLM.",
    "Функция interrupt() полностью замораживает работу графа на текущем супер-шаге, сохраняя всё в checkpointer. Чтобы возобновить граф, человек должен отправить объект Command(resume=True)."
]

# ==========================================
# 3. Генерация вопроса через OpenRouter
# ==========================================
def generate_question_via_openrouter(api_key: str, context: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Используем бесплатную модель для создания вопроса
    payload = {
        "model": "google/gemma-2-9b-it:free",
        "messages": [
            {
                "role": "system",
                "content": "Ты - строгий преподаватель по программированию. Твоя задача: прочитать предоставленный текст (контекст RAG) и задать ОДИН сложный проверочный вопрос студенту по этому материалу. Задавай только вопрос, не давай подсказок и вариантов ответа. Напиши вопрос на русском языке."
            },
            {
                "role": "user",
                "content": f"ТЕКСТ ИЗ УРОКА:\n{context}"
            }
        ]
    }
    
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Ошибка API OpenRouter: {response.text}")
        return "Не удалось сгенерировать вопрос."

# ==========================================
# 4. Отрисовка UI
# ==========================================
def render():
    st.header("Урок 19: Интерактивный RAG-Экзамен")
    
    st.markdown("""
    В этом финальном модуле мы применяем концепции на практике. 
    1. **LLM (OpenRouter Free)** читает один из параграфов курса и динамически генерирует проверочный вопрос.
    2. Вы отвечаете текстом.
    3. **Локальный CrossEncoder** (на вашем компьютере) оценивает сходимость вашего ответа с оригинальным параграфом без траты токенов!
    """)
    
    if not HAS_LOCAL_EVAL:
        st.error("⚠️ Для локальной оценки установите библиотеки: `pip install torch sentence-transformers`")
        return
        
    evaluator = load_evaluator()
    
    # Состояния сессии Streamlit
    if "exam_context" not in st.session_state:
        st.session_state.exam_context = ""
    if "exam_question" not in st.session_state:
        st.session_state.exam_question = ""

    api_key = st.text_input("🔑 Введите ваш OpenRouter API Key", type="password")
    
    if st.button("🎲 Сгенерировать новый вопрос", type="primary"):
        if not api_key:
            st.warning("Пожалуйста, введите API ключ.")
            return
            
        with st.spinner("LLM придумывает вопрос по базе знаний..."):
            # RAG: выбираем случайный чанк из базы
            st.session_state.exam_context = random.choice(KNOWLEDGE_BASE)
            # Генерация
            st.session_state.exam_question = generate_question_via_openrouter(api_key, st.session_state.exam_context)
            # Очистка старого ответа юзера из виджета (хак)
            if "student_answer" in st.session_state:
                st.session_state.student_answer = ""
                
    # Если вопрос сгенерирован, показываем поле для ответа
    if st.session_state.exam_question:
        st.info(f"**Вопрос преподавателя:**\n\n{st.session_state.exam_question}")
        
        user_answer = st.text_area("Ваш ответ:", key="student_answer")
        
        if st.button("✅ Проверить ответ локально (Кросс-энкодер)"):
            if not user_answer.strip():
                st.warning("Напишите ответ!")
                return
                
            with st.spinner("Локальная ИИ проверяет ваш ответ..."):
                # Судья (CrossEncoder) сравнивает оригинальный текст урока с ответом студента
                score = evaluator.predict([[st.session_state.exam_context, user_answer]])
                # Превращаем numpy array во float
                score_val = float(score) if not hasattr(score, '__len__') else float(score[0])
                
                # Порог релевантности (зависит от модели, для этой 0.0-1.0 или логиты)
                # У DiTy/cross-encoder-russian-msmarco выход обычно sigmoid или логит. Будем считать > 0.4 успехом
                
                # Поскольку модели переранжирования иногда возвращают сырые логиты (могут быть > 1 или < 0):
                # Прогоним через sigmoid математически на случай логитов
                import math
                prob = 1 / (1 + math.exp(-score_val))
                
                st.markdown("### Результат автопроверки:")
                if prob > 0.5:
                    st.success(f"🎉 Правильно! Вы поняли суть. (Уверенность ИИ: {prob*100:.1f}%)")
                else:
                    st.error(f"❌ Не совсем точно. (Схожесть с эталоном: {prob*100:.1f}%)")
                    st.markdown(f"**Оригинальный текст из урока:**\n_{st.session_state.exam_context}_")
