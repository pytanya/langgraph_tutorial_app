import streamlit as st

def render():
    st.header("Урок 17: Выбор архитектуры (StateGraph vs Functional API)")
    
    st.markdown("""
    Фреймворк постоянно развивается. Изначально LangGraph предоставлял только низкоуровневый `StateGraph`. 
    Недавно разработчики добавили экспериментальный **Functional API**. Давайте разберемся, что выбрать!
    """)

    st.subheader("1. Стандартный Graph API (StateGraph)")
    st.markdown("Это то, что мы изучали все прошлые уроки.")
    st.markdown("""
    **Плюсы:**
    * Глобальный State (единая память для всех узлов).
    * Поддержка циклов (While-loops / Agents) и маршрутизации.
    * Сложные системы прерываний.
    """)
    
    st.subheader("2. Новый Functional API")
    st.markdown("""
    Functional API больше похож на Prefect, Airflow или Celery. Вы описываете пайплайн, используя декораторы `@task` и функцию `@entrypoint`.
    """)
    st.code("""
from langgraph.func import entrypoint, task

@task
def call_llm(text: str):
    return llm.invoke(text)

@task
def save_db(text: str):
    return "Saved!"

# Точка входа определяет жесткий конвейер (Пайплайн)
@entrypoint()
def my_workflow(request: str):
    # Работает как обычный Python-код! Не нужен StateGraph!
    llm_result = call_llm(request).result()
    save_db(llm_result).result()
    return llm_result
    """, language="python")

    st.markdown("""
    **Плюсы Functional API:**
    * Никаких глобальных классов `State` (все данные передаются локально через аргументы функций).
    * Код выглядит как обычный Python.
    * Не нужно вручную строить ветви (Edges) для обычных цепочек (Chains).
    
    **Минусы:**
    * Не поддерживает зацикливание агента (Cycles) сам по себе! Подходит для жестких конвейеров.
    """)

    st.success("✅ **Вывод (Choosing APIs):** Если вы делаете Агента, который может думать и повторять циклы — используйте **StateGraph**. Если вы делаете Прямолинейный процесс (Суммаризация документа -> Сохранение в БД) — проще написать это с помощью **Functional API**.")
