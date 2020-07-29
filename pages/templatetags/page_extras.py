# Django
from django import template

register = template.Library()


@register.filter(name='batch')
def batch(iterable, n=1):
    lenght = len(iterable)
    for ndx in range(0, lenght, n):
        yield iterable[ndx:min(ndx + n, lenght)]
