import random

from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blog_from_cache():
    """
    Функция получения записей из кэша
    """
    if not CACHE_ENABLED:
        blog = list(Blog.objects.filter(is_published=True))
        random.shuffle(blog)
        return blog[:3]
    key = 'blog_list'
    blog = cache.get(key)
    if blog is not None:
        return blog
    blog = list(Blog.objects.filter(is_published=True)[:3])
    random.shuffle(blog)
    cache.set(key, blog)
    return blog[:3]
