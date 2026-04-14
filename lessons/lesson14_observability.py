import streamlit as st

def render():
    st.header("Урок 14: Наблюдаемость (Observability) через Langfuse")
    
    st.markdown("""
    **Observability (Наблюдаемость)** — это возможность видеть всё, что происходит "под капотом" вашего агента.
    Сколько токенов съела LLM? Какая цепочка узлов была вызвана? За какое время ответил API?
    
    По умолчанию LangChain предлагает платную и проприетарную платформу *LangSmith*.
    Однако в Open-Source сообществе стандартом де-факто стала **бесплатная платформа Langfuse**.
    """)

    st.subheader("1. Подключение Langfuse к агентам")
    st.markdown("Langfuse предлагает встроенный Callback Handler для экосистемы LangChain/LangGraph, который автоматически трассирует (Tracing) все события.")
    
    st.code("""
# 1. Установите зависимости
# pip install langfuse

import os
from langfuse.callback import CallbackHandler

# 2. Инициализируем Callback
langfuse_handler = CallbackHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://cloud.langfuse.com" # Или ваш локальный Docker localhost
)

# 3. Передаем обработчик в граф при запуске!
result = agent_graph.invoke(
    {"message": "Транзакция на 500$"}, 
    config={"callbacks": [langfuse_handler]} # <--- Магия здесь
)
    """, language="python")

    st.subheader("2. Что вы увидите в админке Langfuse?")
    st.markdown("""
    После выполнения `invoke()`, в панели управления Langfuse вы получите:
    * **Граф выполнения (Tree of Execution)**: древовидную структуру каждого шага.
    * **Метрики стоимости**: Автоматический подсчет цены вызова (например, $0.003 за вызов GPT-4o).
    * **Задержки (Latency)**: Сколько секунд выполнялся конкретный Tool.
    * **Prompt Playground**: Вы можете скопировать точный промпт, который отправился в LLM, и отредактировать его прямо в Langfuse для тестирования!
    """)
    
    st.info("💡 Langfuse можно установить бесплатно на свой собственный сервер через Docker (`docker compose up`), что обеспечивает 100% изоляцию данных.")
