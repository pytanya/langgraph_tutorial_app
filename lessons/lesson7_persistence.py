import streamlit as st

def render():
    st.header("Урок 7: Долговечность, Память и Человек-в-контуре (Persistence)")
    
    st.markdown("""
    По умолчанию, при вызове `graph.invoke()` LangGraph стирает состояние сразу после завершения работы. 
    Но с использованием **Checkpointer** вы можете наделить вашего агента невидимой базой данных.
    
    ### Зачем нужен Persistence?
    1. **Memory (Память)**: Изоляция диалогов для разных юзеров с помощью уникального `thread_id`.
    2. **Human-in-the-Loop**: Возможность "остановить" граф, запросить у человека апрув (Approval), и продолжить с той же точки.
    3. **Time Travel (Машина времени)**: Возможность вернуть граф на два шага назад и сказать "вот тут LLM ошиблась, переделай этот шаг с вот такими данными".
    """)

    st.subheader("1. Подключение Checkpointer")
    st.code("""
from langgraph.checkpoint.memory import MemorySaver

# Мы сохраняем состояние локально в ОЗУ (MemorySaver)
# Для продакшена стоит использовать SqliteSaver или PostgresSaver
checkpointer = MemorySaver()

# Граф компилируется с указанием хранилища
app = workflow.compile(checkpointer=checkpointer)

# При запуске мы ОБЯЗАТЕЛЬНО передаем thread_id, чтобы система знала, какую память грузить
config = {"configurable": {"thread_id": "customer_123"}}
app.invoke({"message": "Привет!"}, config=config)
    """)

    st.subheader("2. Human-in-the-Loop (Функция Interrupt)")
    st.markdown("""
    Когда агент хочет совершить критически-важное действие (например, потратить деньги с карты или отправить письмо всему отделу), 
    он может выбросить `interrupt()`.
    """)
    st.code("""
from langgraph.types import interrupt

def some_critical_node(state: State):
    # Граф ОСТАНОВИТСЯ на этой строчке! Аппликация вернет паузу.
    human_decision = interrupt({
        "action_required": "Вам нужно проверить этот драфт ответа:",
        "draft": state["draft_response"]
    })
    
    # ...Когда человек пришлет ответ и возобновит работу графа, код продолжится отсюда:
    if human_decision["approved"]:
        return {"status": "success"}
    """)
    
    st.markdown("""
    **Как возобновить работу из кода?**
    Вы вызываете `invoke` еще раз с командой `Command(resume=...)`:
    """)
    st.code("""
from langgraph.types import Command

# Отправляем ответ человека, чтобы граф разморозился
human_response = Command(resume={"approved": True})

# Запускаем тот же тред
app.invoke(human_response, config={"configurable": {"thread_id": "customer_123"}})
    """)

    st.divider()

    st.subheader("3. Долгосрочная память (Long-term Memory Store)")
    st.markdown("""
    Если `thread_id` хранит локальную переписку (Short Term), то как агенту вспомнить, что он разговаривал с вами год назад? 
    Для этого в LangGraph добавили `Store` API (например, `InMemoryStore` или семантический поиск `search()`).
    """)
    st.code("""
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

# Сохранить память для юзера
namespace = ("user_id_123", "memories")
store.put(namespace, "memory_id_1", {"food": "I like pizza!"})

# Узнать всё, что любит юзер
memories = store.search(namespace)
    """)
    
    st.info("💡 **Вывод:** С помощью Checkpointers агент получает *Нить времени* (Thread). С помощью Store агент получает *Мозг* (Долгосрочные факты).")
