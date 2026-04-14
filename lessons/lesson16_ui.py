import streamlit as st

def render():
    st.header("Урок 16: Интеграция с Frontend (React / UI)")
    
    st.markdown("""
    После того как вы задеплоили ваш агент (узнали на прошлом уроке), вы, вероятно, захотите сделать красивый веб-интерфейс для пользователей.
    Официальная документация LangGraph охватывает концепции потоковой передачи событий (Events) на Frontend.
    """)

    st.subheader("1. Подключение к UI (Frontend Overview)")
    st.markdown("""
    Архитектура UI для агентов отличается от обычных REST запросов. Так как агенты иногда "думают" по 10-30 секунд, и могут спрашивать разрешение (Interrupts), вам нужно держать двусторонний канал.
    Лучший способ для соединения Frontend и вашего FastAPI сервера (или LangGraph Cloud) — **Server-Sent Events (SSE)** или **WebSockets**.
    """)
    
    st.code("""
// Пример на React: Подключение к стриминигу агента (SSE)
const startAgentRun = async (message) => {
    const response = await fetch('http://localhost:8000/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    });
    
    const reader = response.body.getReader();
    // Декодируем байты потока по мере их поступления
    // ...
};
    """, language="javascript")

    st.subheader("2. Graph Execution (Жизненный цикл)")
    st.markdown("""
    На фронтенде вам нужно уметь обрабатывать 4 типа состояний (Events):
    1. **`metadata`**: Метаданные о запуске треда.
    2. **`updates`**: Когда узел завершается, он выдает порцию обновленного State.
    3. **`stream`**: Потоковая передача токенов чат-модели поштучно.
    4. **`interrupt`**: Сигнал о том, что нужно показать пользователю UI-кнопки "Разрешить/Отклонить" (Human in the middle).
    """)

    st.info("""
    💡 **Библиотеки для UI**:
    Вместо написания логики с нуля, LangChain предлагает готовые хуки (Hooks) для разработчиков. Обратите внимание на библиотеку `@langchain/langgraph-sdk` (NPM).
    """)
