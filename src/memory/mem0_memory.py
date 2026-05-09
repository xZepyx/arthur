from mem0 import Memory

from memory.base import MemoryProvider


class Mem0Memory(MemoryProvider):
    def __init__(self):
        config = {
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "llama3",
                    "temperature": 0.1,
                },
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "nomic-embed-text",
                },
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "path": "/tmp/mem0",
                },
            },
        }
        self.memory = Memory.from_config(config)

    def add(self, role, content, metadata=None):
        self.memory.add(content, user_id="arthur", metadata=metadata)

    def search(self, query, limit=5):
        results = self.memory.search(query, user_id="arthur", limit=limit)
        return [r["memory"] for r in results]
