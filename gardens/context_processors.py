# Locals
from .models import Garden


def get_all_gardens(request):
    return Garden.objects.all()


def items(request):
    return {
        'all_gardens': get_all_gardens(request),
    }
