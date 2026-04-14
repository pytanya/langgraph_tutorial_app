import streamlit as st

def render():
    st.header("Урок 10: Путешествия во времени (Time Travel)")
    
    st.markdown("""
    Механизм **Checkpointer** не просто сохраняет текущее состояние — он сохраняет снимок (snapshot) **каждого шага супер-степа** (Super-step).
    Это означает, что у вашего графа есть полная история (Git-like system) для всех изменений. Вы можете:
    * Посмотреть, на каком шаге LLM ошиблась.
    * Отредактировать старое состояние.
    * Перезапустить граф, начиная прямо с этой контрольной точки (Fork) в прошлое! 🔙
    """)

    st.subheader("1. Извлечение истории графа")
    st.code("""
# Получаем историю всех шагов для конкретного треда
config = {"configurable": {"thread_id": "customer_123"}}

# graph.get_state_history вернет итератор "Снимков"
history = list(agent_graph.get_state_history(config))

# Мы можем найти чекпойнт, который нас интересует
for snapshot in history:
    print(f"Шаг № {snapshot.metadata['step']} | Текущие данные: {snapshot.values}")
    print(f"Уникальный ID чекпойнта (Хэш): {snapshot.config['configurable']['checkpoint_id']}")
    """, language="python")

    st.subheader("2. Возврат в прошлое (Replay / Fork)")
    st.markdown("""
    Когда мы берем старый `checkpoint_id` из прошлого шага и запускаем `graph.invoke()` с этим ID, мы фактически создаем **Форк (Разветвление)**.
    """)

    st.code("""
# Хотим откатиться на шаг № 2, где произошла ошибка
bad_checkpoint = history[-2] # Допустим, это шаг до падения
old_config = bad_checkpoint.config

# Если мы передадим old_config в invoke НЕ ВЫЗЫВАЯ update_state,
# Граф просто продолжит работу (Replay) с этого старого снимка!
result = agent_graph.invoke(None, config=old_config)
    """, language="python")

    st.subheader("3. Как исправить ошибку машины перед откатом?")
    st.markdown("""
    Часто нужно не просто запустить из прошлого, но и сказать *"Я сам отредактировал JSON, продолжай с моими правками"*.
    """)
    st.code("""
# 1. Загружаем старый снимок (машина времени)
checkpoint = graph.get_state(old_config)

# 2. Обновляем статус ОПРЕДЕЛЕННОГО узла с помощью update_state
# Это работает как "Git Commit"
new_config = graph.update_state(
    old_config, 
    {"messages": ["Я, как человек, решил что тут должен быть другой ответ."]}
)

# 3. Возобновляем работу с новым форкнутым состояния
graph.invoke(None, config=new_config)
    """, language="python")
