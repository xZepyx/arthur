class MemoryProvider:
    def add(self, role, content, metadata=None):
        raise NotImplementedError

    def search(self, query, limit=5):
        raise NotImplementedError

    def get_context_message(self, query):
        results = self.search(query)
        if not results:
            return None
        return {
            "role": "system",
            "content": (
                "Here is relevant context from past conversations:\n"
                + "\n".join(results)
            ),
        }

    def store_conversation(self, user_msg, assistant_reply):
        self.add("user", user_msg)
        self.add("assistant", assistant_reply)
