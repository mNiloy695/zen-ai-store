#product form cache
from django.core.cache import cache
from .models import Product
def get_product_from_cache(user):
    cache_key=f"products_user_{user.id}"
    products=cache.get(cache_key)
    cache.set(cache_key, products, timeout=60*5)
    if products is None:
        products=Product.objects.filter(user=user).select_related('user').all()
        cache.set(cache_key, products, timeout=60*60)
    return products
