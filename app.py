import streamlit as st

st.set_page_config(page_title="Академия LangGraph", page_icon="🕸️", layout="wide")
st.title("🕸️ Интерактивный учебник: Создание Агентов на LangGraph")

from lessons import (
    lesson1_basics, lesson2_reducers, lesson3_edges, lesson5_thinking, 
    lesson6_workflows, lesson4_frameworks, lesson7_durable, lesson8_memory, 
    lesson9_interrupts, lesson10_time_travel, lesson11_subgraphs,
    lesson12_streaming, lesson13_structure, lesson14_observability, 
    lesson15_deploy, lesson16_ui, lesson17_apis, lesson18_pregel, lesson19_finish
)

options = [
    "--- Выберите модуль ---",
    "--- Модуль 1: Основы ---",
    "Урок 1: Введение (StateGraph)",
    "Урок 2: Редьюсеры (State)",
    "Урок 3: Маршрутизация (Edges)",
    "Урок 4: Замысел (Thinking in LangGraph)",
    "Урок 5: Workflows vs Agents",
    "Урок 6: Интеграция Навыков (Tools)",
    "--- Модуль 2: Память и Время ---",
    "Урок 7: Отказоустойчивость (Durable)",
    "Урок 8: Долгосрочная память (ChromaDB)",
    "Урок 9: Остановка (Human-in-the-Loop)",
    "Урок 10: Путешествие во времени (Time Travel)",
    "--- Модуль 3: Масштаб и Деплой ---",
    "Урок 11: Вложенные графы (Subgraphs)",
    "Урок 12: Потоковая передача (Streaming)",
    "Урок 13: Структура проекта и Тесты",
    "Урок 14: Наблюдаемость (Langfuse)",
    "Урок 15: Деплой через FastAPI",
    "--- Модуль 4: API и Фронтенд ---",
    "Урок 16: Обзор UI-интеграций",
    "Урок 17: Functional vs Graph API",
    "Урок 18: Движок Pregel",
    "Урок 19: Завершение курса"
]

st.sidebar.markdown("### Навигация по курсу")
selected = st.sidebar.selectbox("📚 Темы занятий", options)
st.sidebar.info("Используйте выпадающий список для перехода к следующему уроку в меню.")

if selected == "Урок 1: Введение (StateGraph)": lesson1_basics.render()
elif selected == "Урок 2: Редьюсеры (State)": lesson2_reducers.render()
elif selected == "Урок 3: Маршрутизация (Edges)": lesson3_edges.render()
elif selected == "Урок 4: Замысел (Thinking in LangGraph)": lesson5_thinking.render()
elif selected == "Урок 5: Workflows vs Agents": lesson6_workflows.render()
elif selected == "Урок 6: Интеграция Навыков (Tools)": lesson4_frameworks.render()
elif selected == "Урок 7: Отказоустойчивость (Durable)": lesson7_durable.render()
elif selected == "Урок 8: Долгосрочная память (ChromaDB)": lesson8_memory.render()
elif selected == "Урок 9: Остановка (Human-in-the-Loop)": lesson9_interrupts.render()
elif selected == "Урок 10: Путешествие во времени (Time Travel)": lesson10_time_travel.render()
elif selected == "Урок 11: Вложенные графы (Subgraphs)": lesson11_subgraphs.render()
elif selected == "Урок 12: Потоковая передача (Streaming)": lesson12_streaming.render()
elif selected == "Урок 13: Структура проекта и Тесты": lesson13_structure.render()
elif selected == "Урок 14: Наблюдаемость (Langfuse)": lesson14_observability.render()
elif selected == "Урок 15: Деплой через FastAPI": lesson15_deploy.render()
elif selected == "Урок 16: Обзор UI-интеграций": lesson16_ui.render()
elif selected == "Урок 17: Functional vs Graph API": lesson17_apis.render()
elif selected == "Урок 18: Движок Pregel": lesson18_pregel.render()
elif selected == "Урок 19: Завершение курса": lesson19_finish.render()
else:
    st.markdown("### 🎓 Добро пожаловать!")
    st.markdown("Пожалуйста, **выберите урок из выпадающего списка в боковой панели слева**, чтобы начать обучение по курсу LangGraph.")
