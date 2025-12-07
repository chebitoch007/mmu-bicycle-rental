from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Station


class StationListView(LoginRequiredMixin, ListView):
    """
    List all active bicycle stations
    """
    model = Station
    template_name = 'stations/station_list.html'
    context_object_name = 'stations'
    
    def get_queryset(self):
        return Station.objects.filter(is_active=True).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bicycle Stations'
        return context


class StationDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a single station with available bicycles
    """
    model = Station
    template_name = 'stations/station_detail.html'
    context_object_name = 'station'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['available_bicycles'] = self.object.bicycles.filter(status='available')
        return context