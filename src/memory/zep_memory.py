import os
from dotenv import load_dotenv
from zep_python.external_clients.memory import MemoryClient
from zep_python import Message

from memory.base import MemoryProvider

load_dotenv()


class ZepMemory(MemoryProvider):
    def __init__(self):
        api_key = os.getenv("ZEP_API_KEY")
        self.client = MemoryClient(
            api_key=api_key,
        )

    def add(self, role, content, metadata=None):
        self.client.add(
            session_id="arthur",
            messages=[
                Message(role=role, content=content)
            ]
        )

    def search(self, query, limit=5):
        results = self.client.search_sessions(
            query=query,
            limit=limit,
        )
        return [r.summary for r in results if r.summary]
