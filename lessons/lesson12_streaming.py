import streamlit as st

def render():
    st.header("Урок 12: Потоковая передача данных (Streaming)")
    
    st.markdown("""
    Никто не любит ждать ответа от LLM 20 секунд. Пользователи привыкли к эффекту печатной машинки (как в ChatGPT).
    В LangGraph есть несколько крутых способов для потоковой трансляции данных (Streaming).
    """)

    st.subheader("1. Stream (Стримминг шагов графа)")
    st.markdown("""
    Самый базовый метод `.stream()` отдает вам данные **каждый раз, когда один из узлов заканчивает работу**.
    Это круто для отображения прогресса пользователю (например: `[Поиск в интернете...] -> [Чтение статей...] -> [Генерация ответа...]`).
    """)
    
    st.code("""
# Вместо graph.invoke() вызываем graph.stream()
for step_event in graph.stream({"message": "найди курс биткоина"}):
    # step_event содержит название завершенного узла и его выхлоп
    for node_name, node_output in step_event.items():
        print(f"✅ Узел {node_name} завершил работу!")
        print(f"Данные: {node_output}")
    """, language="python")

    st.subheader("2. Astream_events (Потоковая передача Токенов)")
    st.markdown("""
    Если вы хотите транслировать ответ LLM по одной букве (по одному токену), вы должны использовать асинхронный метод `astream_events` (часть LangChain Runnable API).
    
    Он перехватывает события генерации чат-модели ВНУТРИ узлов графа!
    """)

    st.code("""
import asyncio

async def run_streaming():
    # Запускаем стриминг всех событий версии "V2"
    async for event in graph.astream_events({"message": "расскажи сказку"}, version="v2"):
        kind = event["event"]
        
        # Перехватываем именно чат-токены модели
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            # Выводим букву в консоль без переноса строки
            print(chunk.content, end="", flush=True)

asyncio.run(run_streaming())
    """, language="python")

    st.success("✅ **Лайфхак для Streamlit:** В Streamlit вы можете использовать компонент `st.write_stream()` вместе с асинхронными генераторами `astream_events`, чтобы получить красивый живой UI для вашего агента!")
