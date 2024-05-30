import logging

from django.core.cache import cache

from config.settings import CACHE_TTL, CACHE_ENABLED
from newsletter.models import Newsletter

logger = logging.getLogger(__name__)


def get_newsletters_from_cache():
    if not CACHE_ENABLED:
        logger.debug("Cache is not enabled.")
        return Newsletter.objects.all()

    key = 'newsletters_list'
    newsletters = cache.get(key)

    if newsletters is not None:
        logger.debug("Cache hit for key: %s", key)
        return newsletters

    logger.debug("Cache miss for key: %s", key)
    newsletters = Newsletter.objects.all()
    cache.set(key, newsletters, timeout=CACHE_TTL)
    logger.debug("Cache set for key: %s", key)
    return newsletters