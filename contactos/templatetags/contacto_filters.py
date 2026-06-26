from django import template

register = template.Library()

@register.filter
def split_habilidades(value):
    """Convierte una cadena de habilidades separadas por comas en una lista de tokens limpios."""
    if not value:
        return []
    return [habilidad.strip() for habilidad in value.split(',') if habilidad.strip()]
