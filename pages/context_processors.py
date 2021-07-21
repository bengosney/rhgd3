# First Party
from modulestatus import ModelStatus

# Locals
from .forms import ContactForm
from .models import HomePageHeader, node


def get_nav_items(request):
    nodes = node.objects.all().filter(status=ModelStatus.LIVE_STATUS)

    id = 0
    for nav_node in nodes:
        if nav_node.url == request.get_full_path():
            nav_node.nav_class = "current"
            id = nav_node.lft
            break

    for nav_node in nodes:
        if nav_node.lft < id and nav_node.rght > id:
            nav_node.nav_class = "current"

    return nodes


def get_breadcrumbs(request):
    full_path = request.get_full_path()

    if full_path == "/":
        return None

    for nav_node in node.objects.all():
        if nav_node.url == full_path:
            return nav_node.get_ancestors(include_self=True)


def get_contact_form(request):
    return ContactForm()


def nav_items(request):
    return {
        "nav_items": get_nav_items(request),
        "breadcrumbs": get_breadcrumbs(request),
        "footer_contact_form": get_contact_form(request),
    }


def header_image(request):
    image = HomePageHeader.getCurrentImage()

    if image is not None:
        return {
            "header_image": image,
            "header_image_url": image.image.url,
            "header_image_position": image.position,
        }

    return {
        "header_image": None,
        "header_image_url": None,
        "header_image_position": None,
    }
