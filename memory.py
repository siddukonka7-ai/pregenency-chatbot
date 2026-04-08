user_memory = {
    "trimester": None,
    "last_topic": None
}

def update_memory(key, value):
    user_memory[key] = value

def get_memory(key):
    return user_memory.get(key)