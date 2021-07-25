# Locals
from .models import Garden


def items(request):
    return {
        "all_gardens": Garden.objects.all(),
    }
