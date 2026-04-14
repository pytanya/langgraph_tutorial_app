import streamlit as st

def render():
    st.header("Урок 13: Структура проекта и Тестирование (App Structure & Test)")
    
    st.markdown("""
    Когда ваш агент вырастает из "Jupyter Notebook скрипта" в настоящий Production-ready сервис,
    Вам нужно правильно его организовать.
    """)

    st.subheader("1. Правильная структура директорий (Application Structure)")
    st.markdown("Согласно официальным рекомендациям LangGraph, проект агента должен делиться на такие модули:")
    
    st.code("""
my_agent/
│
├── agent.py         # 1. Сам StateGraph, добавление узлов и компиляция graph = builder.compile()
├── state.py         # 2. Определение TypedDict для состояния
├── nodes.py         # 3. Функции-узлы графа (логика)
├── tools.py         # 4. Внешние инструменты (@tool)
├── config.py        # 5. Промпты, глобальные настройки и конфигурации LLM
│
├── requirements.txt
└── tests/           # 6. Папка юнит-тестов
    """, language="python")
    st.write("С таким разбиением вы можете легко тестировать отдельно узлы (обычные python-функции), отдельно инструменты и отдельно граф в сборе.")

    st.subheader("2. Тестирование Агентов (Testing)")
    st.markdown("""
    Тестировать недетерминированные LLM сложно. Самый лучший способ тестирования в LangGraph — это **перехват узлов и заглушки (Mocks)**.
    """)

    st.markdown("Вы можете передавать 'mock' данные напрямую в узел в тестах, не запуская весь граф:")
    st.code("""
def test_search_node():
    # Мы тестируем только функцию search_node из nodes.py
    fake_state = {"user_query": "погода в Москве"}
    
    # Запускаем узел
    result = search_node(fake_state)
    
    # Узел должен был найти данные и вернуть словарь
    assert "weather_data" in result
    assert result["weather_data"].temp == 20
    """, language="python")

    st.markdown("Для тестирования всего графа вы можете замокать LLM-запросы через LangChain FakeLLM:")
    st.code("""
from langchain_community.chat_models import FakeListChatModel

# Имитируем ответы от GPT
fake_llm = FakeListChatModel(responses=["Привет!", "Погода хорошая."])

# Тестируем граф с фейковой моделью (экономим деньги и не ждем API)
# ... graph.invoke({"messages": [...]})
    """, language="python")
