import streamlit as st
import time
import random

def render():
    st.header("Урок 6: Паттерны рабочих процессов (Workflows vs Agents)")
    
    st.markdown("""
    Документация LangGraph строго разделяет **Workflows** (рабочие процессы) и **Agents** (автономные агенты):
    
    *   **Workflows (Системы):** Имеют предсказуемый маршрут, состоящий из четких шагов. Вы точно знаете, что "Узел А перейдет в Узел Б". Это отлично для корпоративных пайплайнов (например, парсинг резюме -> оценка -> отправка email).
    *   **Agents (Агенты):** Динамичны, и только LLM решает, куда пойдет маршрут и какие инструменты использовать (обычно это зацикленная структура).
    
    Давайте рассмотрим два важнейших паттерна Workflows.
    """)

    st.subheader("Паттерн 1: Параллельное исполнение (Parallelization)")
    st.markdown("Позволяет выполнить 3 разных запроса к LLM одновременно, чтобы ускорить работу. Мы просто проводим ветки (edges) из START во все три узла, а потом сводим их в `aggregator`.")
    st.image('https://langchain-ai.github.io/langgraph/static/workflows-parallelization.png', caption="Parallelization", width=300)
    
    st.code("""
builder.add_edge(START, "call_llm_1")
builder.add_edge(START, "call_llm_2")
builder.add_edge(START, "call_llm_3")

builder.add_edge("call_llm_1", "aggregator")
builder.add_edge("call_llm_2", "aggregator")
builder.add_edge("call_llm_3", "aggregator")
    """)

    st.subheader("Паттерн 2: Оркестратор и Работники (Orchestrator-Worker)")
    st.markdown("""
    Когда мы не знаем заранее, сколько задач нужно выполнить. Оркестратор генерирует "План", и мы динамически запускаем нужное количество воркеров! 
    Это делается с помощью специального API `Send()`.
    """)
    
    st.code("""
from langgraph.types import Send

def assign_workers(state):
    # Допустим, оркестратор решил, что рапорт состоит из 3-х секций
    # Эта функция динамически создаст 3 параллельных узла "write_section"
    return [Send("write_section", {"section_topic": s}) for s in state["sections"]]

builder.add_conditional_edges("orchestrator", assign_workers)
    """)

    st.divider()
    
    st.write("🚀 **Симуляция Orchestrator-Worker**")
    if st.button("Запустить симуляцию Orchestrator-Worker"):
        from typing import TypedDict, Annotated, List
        import operator
        from langgraph.graph import StateGraph, START, END
        from langgraph.types import Send
        
        class State(TypedDict):
            sections: List[str]
            completed_text: Annotated[list, operator.add]
            
        def orchestrator(s: State):
            st.write("🧠 **Оркестратор**: Решил написать книгу про животных из двух глав: [Коты, Собаки]")
            return {"sections": ["Глава: Коты", "Глава: Собаки"]}
            
        def worker(s: dict): # Worker принимает только свой кусочек State
            topic = s["section_topic"]
            time.sleep(1)
            return {"completed_text": [f"Текст для '{topic}'"]}
            
        def assign(s: State):
            # API Send: отправляет конкретные данные на узел 'worker'
            st.write(f"🔄 **Маршрутизатор**: Распаковываю план и запускаю {len(s['sections'])} воркеров параллельно!")
            return [Send("worker", {"section_topic": sec}) for sec in s["sections"]]

        builder = StateGraph(State)
        builder.add_node("orchestrator", orchestrator)
        builder.add_node("worker", worker)
        
        builder.add_edge(START, "orchestrator")
        builder.add_conditional_edges("orchestrator", assign)
        builder.add_edge("worker", END)
        
        graph = builder.compile()
        
        result = graph.invoke({"sections": [], "completed_text": []})
        st.success("Симуляция завершена!")
        st.json(result["completed_text"])
