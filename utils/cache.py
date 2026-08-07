from django.core.cache import cache

from utils.logger import logger


class CacheService:
    @staticmethod
    def get_or_set(key, callback, timeout=3600):
        data = cache.get(key)
        if data is None:
            logger.debug(f"Кэш промах для ключа: {key}")
            data = callback()
            cache.set(key, data, timeout)
            logger.debug(f"Кэш сохранен для ключа: {key}")
        else:
            logger.debug(f"Кэш попадание для ключа: {key}")
        return data

    @staticmethod
    def invalidate(key):
        cache.delete(key)
        logger.debug(f"Кэш очищен для ключа: {key}")

    @staticmethod
    def invalidate_pattern(pattern):
        from django_redis import get_redis_connection

        conn = get_redis_connection("default")
        keys = conn.keys(f"*{pattern}*")
        if keys:
            conn.delete(*keys)
            logger.debug(f"Очищено {len(keys)} ключей кэша по шаблону: {pattern}")
