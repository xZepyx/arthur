def create_memory(name):
    if name == "none":
        return None
    if name == "mem0":
        from memory.mem0_memory import Mem0Memory
        return Mem0Memory()
    if name == "zep":
        from memory.zep_memory import ZepMemory
        return ZepMemory()
    raise ValueError(f"Unknown memory backend: {name}")
