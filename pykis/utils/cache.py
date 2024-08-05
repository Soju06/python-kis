__all__ = [
    "cached",
    "set_cache",
    "get_cache",
]


def cached(fn):
    def wrapper(*args, **kwargs):
        self = args[0]
        cache_key = f"__{fn.__name__}"

        if not hasattr(self, cache_key):
            setattr(self, cache_key, fn(*args, **kwargs))

        return getattr(self, cache_key)

    return wrapper


def set_cache(obj: object, key: str, value: object):
    setattr(obj, f"__{key}", value)


def get_cache(obj: object, key: str, default: object = None):
    return getattr(obj, f"__{key}", default)
