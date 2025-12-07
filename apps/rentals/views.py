from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Reservation, Rental
from .forms import RentalReturnForm, RentalFilterForm
from apps.bicycles.models import Bicycle
from core.email import send_reservation_email, send_rental_start_email, send_rental_end_email


class ReserveBicycleView(LoginRequiredMixin, View):
    """
    Reserve a bicycle
    """
    def post(self, request, slug):
        bicycle = get_object_or_404(Bicycle, slug=slug)
        
        # Check if user can rent
        if not request.user.can_rent:
            messages.error(request, 'You are not eligible to rent bicycles at this time.')
            return redirect('bicycles:detail', slug=slug)
        
        # Check if user already has an active reservation
        if request.user.has_active_reservation:
            messages.error(request, 'You already have an active reservation.')
            return redirect('rentals:reservation-active')
        
        # Check if bicycle is available
        if not bicycle.is_available:
            messages.error(request, 'This bicycle is not available.')
            return redirect('bicycles:detail', slug=slug)
        
        # Create reservation
        reservation = Reservation.objects.create(
            user=request.user,
            bicycle=bicycle,
            station=bicycle.current_station
        )
        
        # Mark bicycle as reserved
        bicycle.mark_as_reserved()
        
        # Send confirmation email
        send_reservation_email(reservation)
        
        messages.success(
            request,
            f'Bicycle reserved successfully! You have 30 minutes to pick it up from {bicycle.current_station.name}.'
        )
        
        return redirect('rentals:reservation-detail', pk=reservation.id)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    """
    View reservation details
    """
    model = Reservation
    template_name = 'rentals/reservation_detail.html'
    context_object_name = 'reservation'
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reservation Details'
        context['can_pick_up'] = self.object.is_active
        return context


class ActiveReservationView(LoginRequiredMixin, DetailView):
    """
    View active reservation
    """
    template_name = 'rentals/reservation_active.html'
    context_object_name = 'reservation'
    
    def get_object(self):
        return Reservation.objects.filter(
            user=self.request.user,
            status='active'
        ).first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active Reservation'
        return context


class CancelReservationView(LoginRequiredMixin, View):
    """
    Cancel a reservation
    """
    def post(self, request, pk):
        reservation = get_object_or_404(
            Reservation,
            pk=pk,
            user=request.user,
            status='active'
        )
        
        reservation.cancel()
        messages.success(request, 'Reservation cancelled successfully.')
        
        return redirect('bicycles:list')


class StartRentalView(LoginRequiredMixin, View):
    """
    Start rental from a reservation
    """
    def post(self, request, pk):
        reservation = get_object_or_404(
            Reservation,
            pk=pk,
            user=request.user,
            status='active'
        )
        
        # Check if reservation is still active
        if reservation.is_expired:
            reservation.expire()
            messages.error(request, 'This reservation has expired.')
            return redirect('bicycles:list')
        
        # Create rental
        rental = Rental.objects.create(
            user=request.user,
            bicycle=reservation.bicycle,
            reservation=reservation,
            pickup_station=reservation.station,
            hourly_rate=reservation.bicycle.hourly_rate
        )
        
        # Convert reservation to picked-up
        reservation.convert_to_rental()
        
        # Mark bicycle as in-use
        reservation.bicycle.mark_as_in_use()
        
        # Send rental start email
        send_rental_start_email(rental)
        
        messages.success(
            request,
            f'Rental started! Enjoy your ride. Hourly rate: KES {rental.hourly_rate}'
        )
        
        return redirect('rentals:active')


class ActiveRentalView(LoginRequiredMixin, DetailView):
    """
    View active rental
    """
    template_name = 'rentals/rental_active.html'
    context_object_name = 'rental'
    
    def get_object(self):
        return Rental.objects.filter(
            user=self.request.user,
            status='active'
        ).select_related('bicycle', 'pickup_station').first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active Rental'
        if self.object:
            context['current_cost'] = self.object.calculate_cost()
        return context


class RentalReturnView(LoginRequiredMixin, FormView):
    """
    Return a rented bicycle
    """
    template_name = 'rentals/rental_return.html'
    form_class = RentalReturnForm
    success_url = reverse_lazy('rentals:history')
    
    def get_rental(self):
        return get_object_or_404(
            Rental,
            user=self.request.user,
            status='active'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Return Bicycle'
        context['rental'] = self.get_rental()
        context['estimated_cost'] = context['rental'].calculate_cost()
        return context
    
    def form_valid(self, form):
        rental = self.get_rental()
        
        # Complete the rental
        rental.complete_rental(
            return_station=form.cleaned_data['return_station'],
            return_notes=form.cleaned_data.get('return_notes', ''),
            distance_km=form.cleaned_data.get('distance_km', 0)
        )
        
        # Apply damage fee if provided
        if form.cleaned_data.get('damage_fee'):
            rental.damage_fee = form.cleaned_data['damage_fee']
            rental.calculate_cost()
            rental.save()
        
        # Send rental end email
        send_rental_end_email(rental)
        
        messages.success(
            self.request,
            f'Bicycle returned successfully! Total cost: KES {rental.total_cost:.2f}'
        )
        
        return super().form_valid(form)


class RentalHistoryView(LoginRequiredMixin, ListView):
    """
    View rental history
    """
    model = Rental
    template_name = 'rentals/rental_history.html'
    context_object_name = 'rentals'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Rental.objects.filter(
            user=self.request.user
        ).select_related('bicycle', 'pickup_station', 'return_station').order_by('-start_time')
        
        # Apply filters
        status = self.request.GET.get('status')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if start_date:
            queryset = queryset.filter(start_time__date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(start_time__date__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rental History'
        context['filter_form'] = RentalFilterForm(self.request.GET)
        context['total_rentals'] = self.request.user.get_total_rentals()
        return context


class RentalDetailView(LoginRequiredMixin, DetailView):
    """
    View rental details
    """
    model = Rental
    template_name = 'rentals/rental_detail.html'
    context_object_name = 'rental'
    
    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Rental #{self.object.id}'
        return context


class CheckReservationStatusView(LoginRequiredMixin, View):
    """
    AJAX endpoint to check reservation status
    """
    def get(self, request, pk):
        reservation = get_object_or_404(
            Reservation,
            pk=pk,
            user=request.user
        )
        
        # Check and expire if needed
        if reservation.is_expired and reservation.status == 'active':
            reservation.expire()
        
        return JsonResponse({
            'status': reservation.status,
            'is_active': reservation.is_active,
            'time_remaining': reservation.time_remaining,
        })