#!/usr/bin/env python3
"""Redis client module"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union


class Cache:
    """cache class"""
    def __init__(self) -> None:
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        method that take a key string argument and an optional Callable argument named fn.
        This callable will be used to convert the data back to the desired format.
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """
        Converts bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        Converts bytes to integers
        """
        return int(data)
