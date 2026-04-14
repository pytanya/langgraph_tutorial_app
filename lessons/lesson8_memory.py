import streamlit as st

def render():
    st.header("Урок 8: Долгосрочная семантическая память (Store + ChromaDB)")
    
    st.markdown("""
    В предыдущих уроках вы видели **Checkpointers**. Они отлично подходят для хранения *истории одной беседы (треда)*. 
    Но что если мы хотим, чтобы агент запоминал факты пользователей навсегда (Long-Term Memory) и мог извлекать их в других чатах?
    
    Для этого LangGraph представляет абстракцию **Store (Хранилище)**, которая поддерживает **семантический поиск** по памяти.
    """)
    
    st.subheader("1. Хранилище в оперативной памяти (InMemoryStore)")
    st.markdown("API Хранилища позволяет вам организовывать память по *namespaces* (пространствам имен) и *уникальным ключам*.")
    st.code("""
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

# 1. Записать воспоминание
namespace = ("user_123", "preferences")
store.put(namespace, "memory_id_1", {"food": "I like pizza!"})

# 2. Найти воспоминания по пространству имен
memories = store.search(namespace)
print(memories[0].value) # Выдаст: {"food": "I like pizza!"}
    """, language="python")

    st.subheader("2. Интеграция с векторной базой данных ChromaDB")
    st.markdown("""
    В реальных системах `InMemoryStore` недостаточно. Нам нужен **настоящий семантический поиск** (Semantic Search) —
    чтобы агент мог отправить запрос "Что любит юзер на ужин?", и векторная система нашла память "food: pizza".
    
    Для этого мы используем **ChromaDB**. Мы можем создать кастомный класс `ChromaStore`, унаследовав `BaseStore` из LangGraph.
    """)

    st.code("""
# Пример реализации кастомного Store поверх ChromaDB
import chromadb
from langgraph.store.base import BaseStore, Item

class ChromaStore(BaseStore):
    def __init__(self, collection_name="user_memories"):
        # chromadb локальная с отключенной отправкой телеметрии
        self.client = chromadb.PersistentClient(settings=chromadb.config.Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def put(self, namespace: tuple, key: str, value: dict, index=None):
        # Превращаем кортеж namespace в строку для метаданных
        ns_string = "/".join(namespace)
        
        # Индексируем в ChromaDB
        self.collection.add(
            ids=[f"{ns_string}_{key}"],
            documents=[str(value)], # Документ для семантического поиска
            metadatas=[{"namespace": ns_string, "key": key}]
        )

    def search(self, namespace: tuple, query: str = None, limit: int = 10):
        ns_string = "/".join(namespace)
        if query:
            # Семантический поиск по смыслу!
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where={"namespace": ns_string}
            )
            return results["documents"]
        # ... логика дефолтного фильтра
    """, language="python")

    st.info("""
    💡 **Как передать Store агенту?**
    При компиляции графа мы передаем его как параметр:
    `graph = builder.compile(checkpointer=MemorySaver(), store=ChromaStore())`
    Внутри узла вы будете иметь доступ к хранилищу через конфигурацию: `config['store']` (или через аннотацию InjectedStore).
    """)
