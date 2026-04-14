import streamlit as st

def render():
    st.header("Урок 9: Прерывание графа (Interrupts и Human-in-the-Loop)")
    
    st.markdown("""
    **Human-in-the-loop (Человек в контуре)** — критическая фича для надежных AI-приложений. 
    Если ваш агент собирается:
    1. Отправить письмо по email 📧
    2. Скачать/удалить файл 🗑️
    3. Сделать транзакцию по API 💳
    
    Вы захотите **приостановить** агентскую цепочку и запросить одобрение (Approval) от живого человека.
    В LangGraph для этого используется метод `interrupt()`.
    """)

    st.subheader("1. Как работает interrupt()")
    st.markdown("В тот момент, когда `interrupt()` вызывается внутри узла графа, **выполнение графа полностью замораживается**, а текущее состояние сохраняется в базу (через *checkpointer*).")
    
    st.code("""
from langgraph.types import interrupt

def review_node(state: State):
    # Если мы вызываем interrupt(), график делает паузу!
    user_decision = interrupt({
        "question": "График заморожен. Одобряете ли вы отправку этого текста?",
        "draft_text": state["email_body"]
    })
    
    # Сюда мы вернемся только когда человек сделает resume()
    if user_decision == "approve":
        return {"status": "sending"}
    else:
        return {"status": "cancelled"}
    """, language="python")

    st.subheader("2. Как возобновить работу (Resume)")
    st.markdown("Мы должны использовать объект `Command()` из `langgraph.types`, чтобы передать ответ пользователя обратно внутрь замороженного узла.")
    
    st.code("""
from langgraph.types import Command

# Пользователь нажал мышкой на кнопку "Одобрить" в UI (например, Streamlit)
# Возобновляем граф для того же thread_id, передавая объект Command
response = Command(resume="approve")

agent_app.invoke(response, config={"configurable": {"thread_id": "123"}})
    """, language="python")

    st.warning("""
    ⚠️ **Важное правило Архитектуры:**
    Всё, что написано В ДО начала `interrupt()` внутри узла, будет **выполнено повторно** при возобновлении!
    Поэтому `interrupt()` должен стоять в самой первой строчке вашего узла, либо узлы с интерраптами должны быть выделены в автономные маленькие Node, чтобы случайно не потратить токены на LLM дважды.
    """)
