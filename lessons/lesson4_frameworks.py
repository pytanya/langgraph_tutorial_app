import streamlit as st

def render():
    st.header("Урок 4: Фреймворки и Tools (LangChain / PydanticAI)")
    
    st.markdown("""
    В реальной жизни узлы (Nodes) — это вызовы LLM (Large Language Model) 
    и исполнение навыков (Tools). Мы подошли к самому вкусному!
    
    Внутри графа LangGraph как правила работают связки LangChain (для инструментов) 
    или других фреймворков. LangGraph предоставляет волшебный пребилд `ToolNode`.
    
    ### LangChain Интеграция ("Золотой стандарт")
    Используется абстракция `ToolNode`, которая автоматически вызовет функции-навыки, 
    если агент попросил их вызвать в предыдущем ответе.
    """)
    st.code("""
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def get_weather(city: str):
    '''Получает погоду'''
    return "Солнечно"

# Узел инструментов сам знает, как вызывать get_weather
tools_node = ToolNode([get_weather])

# Мы используем готовый tools_condition, который сам проверяет:
# Если LLM вернула tool_calls -> идем в tools_node
# Если LLM написала обычный текст -> идем в END (конец)
builder.add_conditional_edges("agent_node", tools_condition)
    """, language="python")
    
    st.markdown("""
    ### PydanticAI интеграция
    Если вы используете **PydanticAI**, вы не можете напрямую засунуть его в `ToolNode` от LangChain, 
    так как PydanticAI имеет свой внутренний граф-схему (RunContext и т.п.).
    Но вы всегда можете создать кастомный Node-обертку:
    """)
    st.code("""
from pydantic_ai import Agent

# Изолированный агент на PydanticAI
p_agent = Agent("openai:gpt-4o")

@p_agent.tool
def get_name(ctx): return "Иван"

# Узел (Node) для графа LangGraph:
def pydantic_node(state: State):
    # Вызываем Pydantic агента ВНУТРИ узла LangGraph
    response = p_agent.run_sync(state["message"])
    # Возвращаем результат обратно в State графа LangGraph
    return {"message": response.data}
    """, language="python")
    
    st.info("💡 **Вывод:** Используйте LangGraph как «Макро-Архитектуру» предприятия, а внутри его узлов пишите логику на том, что больше нравится: LangChain для готовых инструментов, или PydanticAI для строгой типизации!")

    st.divider()
    st.success("🎉 Вы прошли ускоренный курс академии LangGraph! Теперь вы готовы собирать агентов.")
