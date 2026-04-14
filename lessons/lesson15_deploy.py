import streamlit as st

def render():
    st.header("Урок 15: Деплой Агента (Запуск через FastAPI)")
    
    st.markdown("""
    Официальная документация LangGraph предлагает использовать проприетарное облако *LangGraph Cloud* для деплоя агентов в виде API.
    Но в большинстве коммерческих и пет-проектов разработчики хотят **деплоить графы на своих серверах бесплатно**, с использованием популярных фреймворков вроде **FastAPI**.
    """)

    st.subheader("1. Как превратить граф в REST API")
    st.markdown("""
    У вас уже есть скомпилированный граф (например, `agent_graph`).
    Всё, что вам нужно — обернуть его метод `invoke` (или `stream`) в Pydantic модель и FastAPI роут.
    """)
    
    st.code("""
# pip install fastapi uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from my_agent.agent import agent_graph # Импорт вашего графа

app = FastAPI(title="My LangGraph Agent API")

# 1. Pydantic модель для входящего запроса
class AgentRequest(BaseModel):
    message: str
    thread_id: str

# 2. Роут для инвока агента
@app.post("/chat")
async def chat_with_agent(req: AgentRequest):
    # Настраиваем конфигурацию для изоляции пользователей (память треда)
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # Запускаем граф
    result = agent_graph.invoke({"messages": [req.message]}, config=config)
    
    # Возвращаем последнее сообщение из state
    return {"reply": result["messages"][-1].content}

# Запуск сервера: uvicorn main:app --reload
    """, language="python")

    st.subheader("2. Что учесть при деплое?")
    st.markdown("""
    * **Базы данных для State**: Использовать `MemorySaver()` в продакшене (FastAPI) небезопасно, так как при перезапуске сервера (Uvicorn workers) оперативная память сотрется. Используйте `PostgresSaver` из пакета `langgraph-checkpoint-postgres`!
    * **Concurrency (Многопоточность)**: Вызывайте синхронный метод `invoke()` через `await graph.ainvoke()`, чтобы не заблокировать веб-сервер множественными запросами от других пользователей.
    * **Streaming (Потоковый ответ)**: В FastAPI вы можете возвращать `StreamingResponse`, объединяя его с генератором `graph.astream_events()`, реализуя настоящий чат с эффектом печатной машинки!
    """)
