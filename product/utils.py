import logging
import time

def log_execution_time(func):
    
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(f"performance.{func.__module__}.{func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000  # ms
        logger.info(f"Executed {func.__name__} in {duration:.2f} ms")
        return result
    return wrapper


from django.core.cache import cache

def get_product_from_cache(user):
    from .models import Product
    cache_key = f"products_user_{user.id}"
    product_ids = cache.get(cache_key)
    if product_ids is None:
        product_ids = list(
            Product.objects.filter(user=user).values_list('id', flat=True)
        )
        cache.set(cache_key, product_ids, timeout=300)
    if product_ids:
        return Product.objects.filter(id__in=product_ids).select_related('user')
    else:
        return Product.objects.none()

