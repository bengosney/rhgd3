# Locals
from .models import message


def messages(request):
    return {
        "banner_messages": message.get_messages(getattr(request, "session", {})),
    }
