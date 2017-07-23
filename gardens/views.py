from vanilla import DetailView, ListView
from .models import Garden
from pages.decorators import register_list_view


@register_list_view
class GardenList(ListView):
    model = Garden
    template_name = 'gardens/list.html'


class GardenDetail(DetailView):
    model = Garden
    template_name = 'gardens/details.html'
    lookup_field = 'slug'
