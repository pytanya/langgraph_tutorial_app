import streamlit as st

def render():
    st.header("Урок 11: Вложенные графы (Subgraphs)")
    
    st.markdown("""
    Когда ваш агент становится слишком сложным (сотни узлов), держать всё в одном графе StateGraph невозможно.
    Поэтому LangGraph позволяет **вкладывать одни графы в другие**. Скомпилированный граф ведет себя точно так же, как обычная Python-функция!
    """)

    st.subheader("1. Зачем нужны Subgraphs?")
    st.markdown("""
    * **Инкапсуляция:** Разделение логики (например, один граф ищет информацию в интернете, а другой — отвечает за оплату).
    * **Командная работа:** Разные команды разработчиков пишут разные графы, а потом вы объединяете их в один Главный (Parent) граф.
    * **Локальный State:** Вложенный граф может иметь **свой собственный State**, не засоряя мусором глобальное состояние!
    """)
    
    st.code("""
# 1. Создаем дочерний граф
child_builder = StateGraph(ChildState)
child_builder.add_node("search_db", search_node)
child_graph = child_builder.compile()

# 2. Создаем Главный граф
parent_builder = StateGraph(ParentState)
parent_builder.add_node("manager", manager_node)

# 🚀 Мы можем добавить целый скомпилированный граф как обычный УЗЕЛ!
parent_builder.add_node("research_team", child_graph)

parent_builder.add_edge("manager", "research_team")
parent_graph = parent_builder.compile()
    """, language="python")

    st.subheader("2. Как передаются данные (State) между графами?")
    st.markdown("""
    Если у родительского и дочернего графа используются разные ключи (например, `ParentState` и `ChildState`), нам нужно написать **Узел-Адаптер (Wrapper API)**.
    """)

    st.code("""
# Функция-обертка для запуска вложенного графа с трансляцией State
def call_research_subgraph(state: ParentState):
    # Берем данные из родителя
    query = state["user_question"]
    
    # Запускаем дочерний граф
    child_result = child_graph.invoke({"search_query": query})
    
    # Возвращаем результат обратно в формате родителя
    return {"research_summary": child_result["found_documents"]}

parent_builder.add_node("research_team_node", call_research_subgraph)
    """, language="python")

    st.info("💡 **Вывод:** Subgraphs действуют как микросервисы в мире графов. Разбивайте бизнес-домены на вложенные графы для лучшей читаемости кода.")
