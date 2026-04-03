import json
import os
import logging
from time import time
from django.conf import settings
from openai import OpenAI
import time
# from .ulits import log_execution_time
logger = logging.getLogger(__name__)




client = OpenAI(api_key=settings.OPENAI_API_KEY)        

# @log_execution_time
def generate_product_description_and_category(name: str) -> dict:
    try:
        
        prompt = f"""
            Generate:
            1. A catchy 2-sentence marketing description
            2. A product category

            Product: {name}

            Return in JSON format:
            {{
                "description": "...",
                "category": "..."
            }}
            """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content
        logger.info(f"Raw AI Response: {content}")
        
        # Remove markdown code blocks if present
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)

        return {
            "description": result.get("description", ""),
            "category": result.get("category", "General")
        }

    except Exception as e:
        logger.error(f"Error generating product data for '{name}': {str(e)}", exc_info=True)
        return {
            "description": f"{name} is a high-quality product designed for everyday use. It offers reliability and great value.",
            "category": "General"
        }