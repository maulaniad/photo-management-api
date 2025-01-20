from typing import Any, Callable, Iterable

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


class Cache:
    """
    Cache manager that combines Django and django-redis functionalities,
    controlled by the settings.
    """

    @staticmethod
    def get(key: str, default: Any | None = None, version: int | None = None) -> Any:
        """Fetch a given key from the cache."""
        return cache.get(key, default, version)

    @staticmethod
    def get_many(keys: Iterable[str], version: int | None = None) -> dict[str, int | str]:
        """Fetch a bunch of keys from the cache at once."""
        return cache.get_many(keys, version=version)

    @staticmethod
    def get_or_set(key: str, potential_value: Any, version: int | None = None) -> Any | None:
        """Fetch a given key from the cache. If the key does not exist, set it."""
        return cache.get_or_set(key, default=potential_value, version=version)

    @staticmethod
    def set(key: str, value: Any, version: int | None = None) -> None:
        """Set a value in the cache."""
        return cache.set(key, value, version=version)

    @staticmethod
    def set_many(data: dict[str, Any], version: int | None = None) -> list[Any]:
        """Set a bunch of values in the cache at once from a dict of key/value pairs."""
        return cache.set_many(data, version=version)

    @staticmethod
    def delete(key: str, version: int | None = None) -> bool:
        """Delete a given key from the cache."""
        return cache.delete(key, version)

    @staticmethod
    def delete_many(keys: Iterable[str], version: int | None = None) -> None:
        """Delete a bunch of keys from the cache at once."""
        return cache.delete_many(keys, version=version)

    @staticmethod
    def delete_pattern(pattern: str, itersize: int = 100_000) -> None:
        """Deletes all cache entries that match the specified pattern."""
        return cache.delete_pattern(pattern, itersize=itersize)  # type: ignore

    @staticmethod
    def ttl(key: str) -> Any:
        """Retrieves the time-to-live (TTL) of a cache entry."""
        return cache.ttl(key)                                    # type: ignore

    @staticmethod
    def persist(key: str) -> Any:
        """Persist a cache entry with the given key, no longer expires."""
        return cache.persist(key)                                # type: ignore

    @staticmethod
    def expire(key: str, timeout: int = 0) -> Any:
        """Add expiration time to a cache entry, 0 to immediately expire."""
        return cache.expire(key, timeout)                        # type: ignore

    @staticmethod
    def iter_keys(pattern: str) -> list[Any]:
        """Search keys based on pattern."""
        return list(cache.iter_keys(pattern))                    # type: ignore

    @staticmethod
    def has_key(key: str, version: int | None = None) -> bool:
        """Return True if the key is in the cache and has not expired."""
        return cache.has_key(key, version)


def cache_view(key_prefix: str, timeout: int = 900, variation_headers: Iterable[str] | None = None) -> Callable:
    """Decorator for caching the entire view response."""

    def wrapper(view_func: Callable) -> Any:
        decorated_func = method_decorator(cache_page(timeout, key_prefix=key_prefix))(view_func)

        if variation_headers:
            return method_decorator(vary_on_headers(*variation_headers))(decorated_func)

        return decorated_func
    return wrapper


def destroy_cache_view(key_prefix: str):
    """Invalidates all stored view caches for the provided key."""

    key_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*"
    Cache.delete_pattern(key_pattern, itersize=100_000)
