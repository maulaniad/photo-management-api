from typing import Any, Callable, Iterable

from django.core.cache import caches
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


class Cache:
    """
    Cache manager that combines Django and django-redis functionalities,
    controlled mostly by the `settings.py`. Instantiate this class
    and optionally provide the `cache_backend` to use. If not, will use the
    default backend.
    """
    cache_backend = "default"

    def __init__(self, cache_backend: str | None = None):
        if cache_backend:
            self.cache_backend = cache_backend

    def _mins_to_secs(self, timeout_mins: int | None) -> float:
        """Convert minutes to seconds, used by the Cache internal class."""
        if not timeout_mins:
            return settings.CACHES['default']['TIMEOUT']
        return timeout_mins * 60

    def get(self, key: str, default: Any | None = None, version: int | None = None) -> Any:
        """Fetch a given key from the cache."""
        return caches[self.cache_backend].get(key, default, version)

    def get_many(self, keys: Iterable[str], version: int | None = None) -> dict[str, int | str]:
        """Fetch a bunch of keys from the cache at once."""
        return caches[self.cache_backend].get_many(keys, version=version)

    def get_or_set(self, key: str, potential_value: Any, version: int | None = None, timeout_mins: int | None = None) -> Any | None:
        """Fetch a given key from the cache. If the key does not exist, set it."""
        return caches[self.cache_backend].get_or_set(key, default=potential_value, version=version, timeout=self._mins_to_secs(timeout_mins))

    def set(self, key: str, value: Any, version: int | None = None, timeout_mins: int | None = None) -> None:
        """Set a value in the cache."""
        return caches[self.cache_backend].set(key, value, version=version, timeout=self._mins_to_secs(timeout_mins))

    def set_many(self, data: dict[str, Any], version: int | None = None, timeout_mins: int | None = None) -> list[Any]:
        """Set a bunch of values in the cache at once from a dict of key/value pairs."""
        return caches[self.cache_backend].set_many(data, version=version, timeout=self._mins_to_secs(timeout_mins))

    def delete(self, key: str, version: int | None = None) -> bool:
        """Delete a given key from the cache."""
        return caches[self.cache_backend].delete(key, version)

    def delete_many(self, keys: Iterable[str], version: int | None = None) -> None:
        """Delete a bunch of keys from the cache at once."""
        return caches[self.cache_backend].delete_many(keys, version=version)

    def delete_pattern(self, pattern: str, itersize: int = 100_000) -> None:
        """Deletes all cache entries that match the specified pattern."""
        return caches[self.cache_backend].delete_pattern(pattern, itersize=itersize)  # type: ignore

    def ttl(self, key: str) -> Any:
        """Retrieves the time-to-live (TTL) of a cache entry."""
        return caches[self.cache_backend].ttl(key)                                    # type: ignore

    def persist(self, key: str) -> Any:
        """Persist a cache entry with the given key, no longer expires."""
        return caches[self.cache_backend].persist(key)                                # type: ignore

    def expire(self, key: str, timeout: int = 0) -> Any:
        """Add expiration time to a cache entry, 0 to immediately expire."""
        return caches[self.cache_backend].expire(key, timeout)                        # type: ignore

    def iter_keys(self, pattern: str) -> list[Any]:
        """Search keys based on pattern."""
        return list(caches[self.cache_backend].iter_keys(pattern))                    # type: ignore

    def has_key(self, key: str, version: int | None = None) -> bool:
        """Return True if the key is in the cache and has not expired."""
        return caches[self.cache_backend].has_key(key, version)


def cache_view(key_prefix: str, timeout: int = 900, variation_headers: Iterable[str] | None = None, cache_backend: str | None = None) -> Callable:
    """Decorator for caching the entire view response."""

    def wrapper(view_func: Callable) -> Any:
        decorated_func = method_decorator(cache_page(timeout, key_prefix=key_prefix, cache=cache_backend))(view_func)

        if variation_headers:
            return method_decorator(vary_on_headers(*variation_headers))(decorated_func)

        return decorated_func
    return wrapper


def destroy_cache_view(key_prefix: str, cache_backend: str | None = None):
    """Invalidates all stored view caches for the provided key."""

    key_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*"
    Cache(cache_backend).delete_pattern(key_pattern, itersize=100_000)
