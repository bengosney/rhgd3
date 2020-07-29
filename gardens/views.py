# Django
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_list_or_404

# Third Party
from vanilla import DetailView, ListView

# First Party
from pages.decorators import register_list_view

# Locals
from .models import Garden, MaintenanceItem, WorkType


@register_list_view
class GardenList(ListView):
    model = Garden
    template_name = 'gardens/list.html'

    @property
    def url(self):
        return reverse_lazy('gardens:GardenList')

    def get_queryset(self):
        try:
            return get_list_or_404(
                Garden, work_type__slug=self.kwargs["filter_val"])
        except KeyError:
            return super(GardenList, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**self.kwargs)
        context['work_types'] = WorkType.objects.all()

        return context


@register_list_view
class MaintenanceItemView(ListView):
    model = MaintenanceItem
    template_name = 'gardens/maintenanceitems.html'


class MaintenanceItemDetailView(DetailView):
    model = MaintenanceItem
    template_name = 'gardens/maintenancedetails.html'
    lookup_field = 'slug'


class GardenListFiltered(ListView):
    model = Garden
    template_name = 'gardens/list.html'

    def get_queryset(self):
        return Garden.objects.filter(work_type__slug=self.kwargs["slug"])


class GardenDetail(DetailView):
    model = Garden
    template_name = 'gardens/details.html'
    lookup_field = 'slug'
