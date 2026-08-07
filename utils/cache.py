from django.core.cache import cache

from utils.logger import logger


class CacheService:
    @staticmethod
    def get_or_set(key, callback, timeout=3600):
        try:
            data = cache.get(key)
            if data is None:
                logger.debug(f"Кэш промах для ключа: {key}")
                data = callback()
                try:
                    cache.set(key, data, timeout)
                    logger.debug(f"Кэш сохранен для ключа: {key}")
                except Exception as e:
                    logger.warning(f"Не удалось сохранить кэш: {e}")
                return data
            logger.debug(f"Кэш попадание для ключа: {key}")
            return data
        except Exception as e:
            logger.warning(f"Ошибка кэша: {e}, возвращаем данные без кэширования")
            return callback()

    @staticmethod
    def invalidate(key):
        try:
            cache.delete(key)
            logger.debug(f"Кэш очищен для ключа: {key}")
        except Exception as e:
            logger.warning(f"Не удалось очистить кэш: {e}")

    @staticmethod
    def invalidate_pattern(pattern):
        try:
            from django_redis import get_redis_connection

            conn = get_redis_connection("default")
            keys = conn.keys(f"*{pattern}*")
            if keys:
                conn.delete(*keys)
                logger.debug(f"Очищено {len(keys)} ключей кэша по шаблону: {pattern}")
        except Exception as e:
            logger.warning(f"Не удалось очистить кэш по шаблону: {e}")
