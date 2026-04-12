import streamlit as st
import operator
from typing import Annotated, TypedDict
import time

def render():
    st.header("Урок 2: Редьюсеры (Reducers)")
    
    st.markdown("""
    В первом уроке наш словарь State **перезаписывался** на каждом шаге. 
    Но что если мы хотим сохранять **всю историю** переписки? 
    Для этого в LangGraph есть **Редьюсеры** (`Annotated`).
    
    ### Зачем нужен Редьюсер?
    Редьюсер указывает графу: *"Не заменяй это значение, а примени к нему функцию (например, добавь в список)"*.
    """)
    
    st.code("""
import operator
from typing import Annotated, TypedDict

# Annotated[list, operator.add] означает:
# Всякий раз, когда узел возвращает {"messages": ["новое"]},
# оно будет ДОБАВЛЕНО (+) к старому списку, а не перезапишет его!
class State(TypedDict):
    messages: Annotated[list, operator.add]
    """)
    
    st.markdown("### Пример двух узлов")
    st.code("""
from langgraph.graph import StateGraph, START, END

def node_a(state: State):
    return {"messages": ["Сообщение от Узла А"]}
    
def node_b(state: State):
    return {"messages": ["Сообщение от Узла Б"]}
    
builder = StateGraph(State)
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)

# Маршрут: START -> A -> B -> END
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", END)

graph = builder.compile()
    """)
    
    st.divider()
    st.subheader("🚀 Интерактивная Песочница")
    
    if st.button("Проверить Редьюсер", type="primary"):
        class State(TypedDict):
            messages: Annotated[list, operator.add]
            
        def node_a(state: State):
            return {"messages": ["🍎 Узел А добавил Яблоко"]}
            
        def node_b(state: State):
            return {"messages": ["🍌 Узел Б добавил Банан"]}
            
        from langgraph.graph import StateGraph, START, END
        builder = StateGraph(State)
        builder.add_node("node_a", node_a)
        builder.add_node("node_b", node_b)
        builder.add_edge(START, "node_a")
        builder.add_edge("node_a", "node_b")
        builder.add_edge("node_b", END)
        graph = builder.compile()
        
        with st.status("Исполняем граф...", expanded=True) as status:
            st.write("Начало: State пустой или содержит наше базовое значение")
            initial_state = {"messages": ["Начало путешествия!"]}
            result = graph.invoke(initial_state)
            status.update(label="Готово!", state="complete")
            
        st.write("Как видите, массив вырос, хотя каждый узел возвращал всего один элемент в массиве:")
        st.json(result)
