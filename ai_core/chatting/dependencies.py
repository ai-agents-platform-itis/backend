from functools import lru_cache

from .chatting import Chatting


@lru_cache(maxsize=1)
def get_chatting():
    return Chatting()
