#!/usr/bin/env python3
"""Redis client module"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union


class Cache:
    """cache class"""
    def __init__(self):
        """initialize new cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store the input data in Redis using the random key and return the key."""
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key