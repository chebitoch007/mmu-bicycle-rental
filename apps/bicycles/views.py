from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Bicycle, MaintenanceLog
from .forms import BicycleForm, BicycleSearchForm, MaintenanceLogForm


class BicycleListView(LoginRequiredMixin, ListView):
    """
    List all available bicycles with search and filter
    """
    model = Bicycle
    template_name = 'bicycles/bicycle_list.html'
    context_object_name = 'bicycles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Bicycle.objects.select_related('current_station').all()
        
        # Get search parameters
        search = self.request.GET.get('search')
        station = self.request.GET.get('station')
        status = self.request.GET.get('status')
        min_rate = self.request.GET.get('min_rate')
        max_rate = self.request.GET.get('max_rate')
        
        # Apply filters
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(model__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(description__icontains=search)
            )
        
        if station:
            queryset = queryset.filter(current_station_id=station)
        
        if status:
            queryset = queryset.filter(status=status)
        else:
            # Default to showing only available bikes for regular users
            if not self.request.user.is_staff:
                queryset = queryset.filter(status='available')
        
        if min_rate:
            queryset = queryset.filter(hourly_rate__gte=min_rate)
        
        if max_rate:
            queryset = queryset.filter(hourly_rate__lte=max_rate)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Available Bicycles'
        context['search_form'] = BicycleSearchForm(self.request.GET)
        context['total_available'] = Bicycle.objects.filter(status='available').count()
        return context


class BicycleDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a single bicycle
    """
    model = Bicycle
    template_name = 'bicycles/bicycle_detail.html'
    context_object_name = 'bicycle'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.name} - {self.object.model}'
        context['can_reserve'] = (
            self.request.user.can_rent and 
            self.object.is_available and
            not self.request.user.has_active_reservation
        )
        context['recent_rentals'] = self.object.rentals.filter(
            status='completed'
        ).select_related('user')[:5]
        return context


class BicycleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create a new bicycle (Admin only)
    """
    model = Bicycle
    form_class = BicycleForm
    template_name = 'bicycles/bicycle_form.html'
    success_url = reverse_lazy('bicycles:list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Bicycle added successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Bicycle'
        context['button_text'] = 'Add Bicycle'
        return context


class BicycleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update bicycle details (Admin only)
    """
    model = Bicycle
    form_class = BicycleForm
    template_name = 'bicycles/bicycle_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_success_url(self):
        return reverse_lazy('bicycles:detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.success(self.request, 'Bicycle updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit {self.object.name}'
        context['button_text'] = 'Update Bicycle'
        return context


class BicycleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete bicycle (Admin only)
    """
    model = Bicycle
    template_name = 'bicycles/bicycle_confirm_delete.html'
    success_url = reverse_lazy('bicycles:list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Bicycle deleted successfully!')
        return super().delete(request, *args, **kwargs)


class MaintenanceLogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create maintenance log (Admin only)
    """
    model = MaintenanceLog
    form_class = MaintenanceLogForm
    template_name = 'bicycles/maintenance_form.html'
    success_url = reverse_lazy('bicycles:list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        # Mark bicycle as under maintenance
        bicycle = form.cleaned_data['bicycle']
        bicycle.mark_as_maintenance()
        
        messages.success(self.request, 'Maintenance log created successfully!')
        return super().form_valid(form)