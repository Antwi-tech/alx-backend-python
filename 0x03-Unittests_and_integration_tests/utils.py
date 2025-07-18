#!/usr/bin/env python3
"""Generic utilities for github org client."""
import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Dict, Callable

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map

def get_json(url: str) -> Dict:
    response = requests.get(url)
    return response.json()

def memoize(fn: Callable) -> Callable:
    attr_name = "_{}".format(fn.__name__)
    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return property(memoized)
