from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name="currency")
def currency(value):
    """Formata um valor decimal para o formato de moeda brasileira."""
    if value is not None:
        return (
            f"R$ {Decimal(value):,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    return "R$ 0,00"
