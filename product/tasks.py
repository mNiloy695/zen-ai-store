from datetime import time

from celery import shared_task
import logging
import time
from .generate import generate_product_description_and_category
from .utils import log_execution_time

logger = logging.getLogger(__name__)


@shared_task
@log_execution_time
def process_product(product_id):
    from .models import Product
    time.sleep(2)  # Simulate a heavy image processing task for testing purposes
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return f"Product with id {product_id} does not exist."
    ai_response = generate_product_description_and_category(product.name)
    logger.info(f"AI response for product {product_id}: {ai_response}")
    product.description = ai_response.get('description', '')
    product.category = ai_response.get('category', '')
    logger.info(f"Saving product {product_id} with description: {product.description}, category: {product.category}")
    product.save()






