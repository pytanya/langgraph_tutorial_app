import streamlit as st

def render():
    st.header("Урок 5: Психология разработки агентов (Thinking in LangGraph)")
    
    st.markdown("""
    При создании приложения на LangGraph очень важно правильно спроектировать архитектуру (как дробить бизнес-логику на графы и узлы). 
    В этом уроке собраны инсайты из официальной документации [Thinking in LangGraph].
    
    ### 1. State должен быть "сырым" (Keep State Raw)
    Типичная ошибка: сохранять в `State` уже готовый текстовый промпт. 
    **Лучшая практика**: хранить в состоянии *атомарные сырые данные* (словари, флаги, списки), а строковые промпты (Prompt Templates) форматировать **по требованию внутри узла**, прямо перед вызовом LLM.
    
    """)
    
    st.code("""
# ❌ Плохо (State засоряется длинными текстами, тяжело дебажить)
class BadState(TypedDict):
    prompt_history: str

# ✅ Хорошо (Сырые данные)
class EmailAgentState(TypedDict):
    email_content: str
    classification: dict  # {'intent': 'bug', 'urgency': 'high'}
    customer_history: dict
    """, language="python")

    st.markdown("""
    ### 2. Гранулярность узлов (LLM vs Data vs API)
    Разделяйте вызовы к внешним API (базы данных, веб-хуки) и вызовы к LLM на **разные** узлы.
    
    **Зачем?** 
    Если ваш API упадет или вернет ошибку таймаута (Transient error), вы сможете повесить на него `RetryPolicy` (политику автоповторов). Если API и LLM будут в одном узле, при падении API вам придется заново тратить деньги на повторный вызов LLM!
    """)
    
    st.code("""
from langgraph.types import RetryPolicy

# Отдельный узел для парсинга документации (может упасть по 504 таймауту)
workflow.add_node(
    "search_documentation", 
    search_documentation_logic,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0)
)
    """, language="python")

    st.divider()

    st.markdown("""
    ### 3. Обработка ошибок
    В рамках **навыков (Tools)** используйте логику, чтобы возвращать сообщение об ошибке прямо агенту, позволяя модели сделать само-коррекцию, а не ронять всю программу (Exception).
    """)

    st.code("""
def execute_tool(state: State):
    try:
        result = run_tool(state['tool_call'])
        return {"tool_result": result}
    except Exception as e:
        # 🟢 Позволяем LLM увидеть, что пошло не так, и попытаться заново!
        return {"tool_result": f"Tool error: {str(e)}"}
    """)
    st.info("💡 **Вывод:** Проектируйте так, чтобы узлы (Nodes) были маленькими и изолированными (single responsibility), а состояние (State) — строгим и атомарным.")
