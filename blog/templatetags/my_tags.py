from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """
    Фильтр для работы с путями медиафайлов
    """
    if path:
        return f"/media/{path}"
    return "#"
