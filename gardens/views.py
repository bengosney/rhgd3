from vanilla import DetailView, ListView
from .models import Garden
from pages.decorators import register_list_view
from django.core.urlresolvers import reverse_lazy

@register_list_view
class GardenList(ListView):
    model = Garden
    template_name = 'gardens/list.html'

    @property
    def url(self):
        return reverse_lazy('gardens:GardenList')


class GardenDetail(DetailView):
    model = Garden
    template_name = 'gardens/details.html'
    lookup_field = 'slug'
