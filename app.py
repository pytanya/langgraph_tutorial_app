import streamlit as st

st.set_page_config(page_title="Академия LangGraph", page_icon="🕸️", layout="wide")
st.title("🕸️ Интерактивный учебник: Создание Агентов на LangGraph")

import lessons.lesson1_basics as lesson1_basics
import lessons.lesson2_reducers as lesson2_reducers
import lessons.lesson3_edges as lesson3_edges
import lessons.lesson5_thinking as lesson5_thinking
import lessons.lesson6_workflows as lesson6_workflows
import lessons.lesson4_frameworks as lesson4_frameworks
import lessons.lesson7_durable as lesson7_durable
import lessons.lesson8_memory as lesson8_memory
import lessons.lesson9_interrupts as lesson9_interrupts
import lessons.lesson10_time_travel as lesson10_time_travel
import lessons.lesson11_subgraphs as lesson11_subgraphs
import lessons.lesson12_streaming as lesson12_streaming
import lessons.lesson13_structure as lesson13_structure
import lessons.lesson14_observability as lesson14_observability
import lessons.lesson15_deploy as lesson15_deploy
import lessons.lesson16_ui as lesson16_ui
import lessons.lesson17_apis as lesson17_apis
import lessons.lesson18_pregel as lesson18_pregel
import lessons.lesson19_finish as lesson20_finish

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
    "Урок 19: Оценка RAG (Локальные реранкеры)",
    "Урок 20: Завершение курса"
]

st.sidebar.markdown("### Навигация по курсу")
selected = st.sidebar.selectbox("📚 Темы занятий", options)
st.sidebar.info("Используйте выпадающий список для перехода к следующему уроку меню.")

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
elif selected == "Урок 19: Оценка RAG (Локальные реранкеры)":
    import lessons.lesson19_exam as lesson19_exam
    lesson19_exam.render()
elif selected == "Урок 20: Завершение курса": lesson20_finish.render()
elif selected == "--- Модуль 1: Основы ---": 
    st.markdown("## 📖 Модуль 1: Основы")
    st.info("В этом модуле мы изучим базовые концепции LangGraph: стейты (состояния), узлы (рабочие функции), ребра (маршрутизацию) и основные архитектурные паттерны.")
elif selected == "--- Модуль 2: Память и Время ---":
    st.markdown("## 🧠 Модуль 2: Память и Время")
    st.info("В этом модуле мы рассмотрим долговременную память (ChromaDB), контрольные точки потоков и функции ручного перехвата управления (Human-in-the-Loop).")
elif selected == "--- Модуль 3: Масштаб и Деплой ---":
    st.markdown("## 🚀 Модуль 3: Масштаб и Деплой")
    st.info("В этом модуле фокус смещается на архитектуру сложных приложений: вложенные графы, тестирование конфигураций, мониторинг логов (Langfuse) и упаковку в Production (FastAPI).")
elif selected == "--- Модуль 4: API и Фронтенд ---":
    st.markdown("## 🌐 Модуль 4: API и Фронтенд")
    st.info("В этом финальном модуле мы разберем интеграцию фронтенда, внутренний алгоритм Pregel на котором базируется фреймворк, и пройдем финальный экзамен!")
else:
    st.markdown("### 🎓 Добро пожаловать!")
    st.markdown("Пожалуйста, **выберите урок из выпадающего списка в боковой панели слева**, чтобы начать обучение по курсу LangGraph.")
