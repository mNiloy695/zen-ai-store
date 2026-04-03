

from celery import shared_task
import asyncio
from .models import Product
from .generate import generate_product_description_and_category

@shared_task
def process_product(product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return f"Product with id {product_id} does not exist."
    
    ai_response = asyncio.run(generate_product_description_and_category(product.name))
    
    product.description=ai_response.get('description', '')
    product.category=ai_response.get('category', '')
    product.save()
    
    
    
    


