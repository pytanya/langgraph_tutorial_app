import streamlit as st
import time

def render():
    st.header("Урок 1: Базовый конвейер (StateGraph)")
    
    st.markdown("""
    В основе LangGraph лежит концепция **Графа Состояний** (`StateGraph`). 
    Представьте, что ваше приложение — это конвейер (граф), по которому движется коробка с данными (состояние/State).
    Каждый рабочий на конвейере (узел/Node) берет коробку, что-то в ней меняет и передает дальше.
    
    ### 1. Определяем коробку (State)
    Обычно это обычный словарь `TypedDict`.
    """)
    
    st.code("""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str
    """)
    
    st.markdown("### 2. Создаем узлы (Nodes)")
    st.code("""
def node_echo(state: State):
    # Берет старое состояние и возвращает обновление для него
    return {"message": state["message"] + " -> Привет из узла!"}
    """)
    
    st.markdown("### 3. Собираем граф")
    st.code("""
builder = StateGraph(State)
builder.add_node("step_1", node_echo)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", END)

graph = builder.compile()
    """)
    
    st.divider()
    st.subheader("🚀 Интерактивный запуск")
    
    user_input = st.text_input("Введите начальное сообщение:", "Начинаем работу")
    
    if st.button("Запустить граф", type="primary"):
        from typing import TypedDict
        from langgraph.graph import StateGraph, START, END
        
        class State(TypedDict):
            message: str
            
        def node_echo(state: State):
            return {"message": state["message"] + " -> [Узел 1 успешно отработал!]"}
            
        builder = StateGraph(State)
        builder.add_node("step_1", node_echo)
        builder.add_edge(START, "step_1")
        builder.add_edge("step_1", END)
        graph = builder.compile()
        
        with st.spinner("Работает граф..."):
            time.sleep(0.5) # Имитация сложной работы LLM
            initial_state = {"message": user_input}
            result = graph.invoke(initial_state)
            
            st.success("Граф завершил работу!")
            st.json({
                "Начальный State": initial_state,
                "Финальный State": result
            })
