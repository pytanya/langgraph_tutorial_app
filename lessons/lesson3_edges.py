import streamlit as st
import random
import time

def render():
    st.header("Урок 3: Условные Переходы (Conditional Edges)")
    
    st.markdown("""
    Агенты становятся "умными", когда могут принимать решения, куда идти дальше. 
    **Conditional Edges** позволяют вызывать функцию маршрутизации. Эта функция смотрит на `State` и возвращает имя следующего узла.
    """)
    
    st.code("""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    number: int
    
def router_node(state: State):
    return {"number": random.randint(1, 10)}

# Фукнция-маршрутизатор
def route(state: State):
    # Мы смотрим на текущее состояние и принимаем решение!
    if state["number"] > 5:
        return "node_high"
    else:
        return "node_low"
        
builder = StateGraph(State)
builder.add_node("router_node", router_node)
builder.add_node("node_high", lambda s: {"number": s["number"]})
builder.add_node("node_low", lambda s: {"number": s["number"]})

builder.add_edge(START, "router_node")

# Обратите внимание на add_conditional_edges
builder.add_conditional_edges(
    "router_node", # Откуда выходим
    route,         # Функция, решающая, куда идти
                   # В зависимости от того, что вернула функция route, 
                   # перейдем в узел с этим именем.
)
builder.add_edge("node_high", END)
builder.add_edge("node_low", END)
    """)
    
    st.divider()
    st.subheader("🚀 Испытание Маршрутизатора")
    
    if st.button("Бросить кости и маршрутизировать!"):
        from typing import TypedDict
        from langgraph.graph import StateGraph, START, END
        
        class State(TypedDict):
            status: str
            
        def generator(s):
            val = random.choice(["ОТПРАВЛЕНО", "ОШИБКА", "ЖДЕТ"])
            st.write(f"Узел 'генератор' создал статус: **{val}**")
            return {"status": val}
            
        def route_fn(s):
            if s["status"] == "ОШИБКА":
                return "fix_node"
            return "success_node"
            
        def fix_node(s):
            st.write("🔴 Сработала ветка ошибки (Узел починки)!")
            return {"status": "ПОЧИНЕНО"}
            
        def success_node(s):
            st.write("🟢 Сработала успешная ветка!")
            return s
            
        builder = StateGraph(State)
        builder.add_node("generator", generator)
        builder.add_node("fix_node", fix_node)
        builder.add_node("success_node", success_node)
        
        builder.add_edge(START, "generator")
        builder.add_conditional_edges("generator", route_fn)
        builder.add_edge("fix_node", END)
        builder.add_edge("success_node", END)
        
        graph = builder.compile()
        graph.invoke({"status": ""})
