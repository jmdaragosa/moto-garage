from django import template

register = template.Library()


@register.filter
def format_php(value):
    """
    Format number as Philippine Peso.
    Example:
        850 -> ₱850.00
    """

    if value is None:
        return "₱0.00"

    return f"₱{value:,.2f}"