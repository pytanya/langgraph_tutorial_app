import streamlit as st

st.set_page_config(page_title="Академия LangGraph", page_icon="🕸️", layout="wide")

st.title("🕸️ Интерактивный учебник: Создание Агентов на LangGraph")
st.markdown("""
Добро пожаловать в приложение-учебник! Здесь мы шаг за шагом на реальном коде разберем, как создаются современные AI-агенты.
Выберите урок в меню слева.
""")

from lessons import lesson1_basics, lesson2_reducers, lesson3_edges, lesson4_frameworks

tabs = st.sidebar.radio("📚 Выберите раздел", 
       ["Введение в StateGraph", 
        "Редьюсеры (Управление состоянием)", 
        "Маршрутизация (Условные переходы)", 
        "Интеграция Навыков (Tools)"])

if tabs == "Введение в StateGraph":
    lesson1_basics.render()
elif tabs == "Редьюсеры (Управление состоянием)":
    lesson2_reducers.render()
elif tabs == "Маршрутизация (Условные переходы)":
    lesson3_edges.render()
elif tabs == "Интеграция Навыков (Tools)":
    lesson4_frameworks.render()
