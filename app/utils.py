import requests
import os
from dotenv import load_dotenv
from cachetools import TTLCache
import logging

logger = logging.getLogger(__name__)
load_dotenv()

cache = TTLCache(maxsize=100, ttl=3600)  # Cache API results for 1 hour

def get_exchange_rate(base_currency, target_currency):
    try:
        cache_key = f"{base_currency}_{target_currency}"
        if cache_key in cache:
            return cache[cache_key]
        
        api_key = os.getenv('API_KEY')
        if not api_key:
            logger.error("API key not found")
            return 1.0
        
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        rate = data['conversion_rates'].get(target_currency, 1.0)
        cache[cache_key] = rate
        logger.info(f"Fetched exchange rate: {base_currency} to {target_currency} = {rate}")
        return rate
    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        return 1.0

def clear_cache():
    cache.clear()
    logger.info("Cache cleared")
    return True