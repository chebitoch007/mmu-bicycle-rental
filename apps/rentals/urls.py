from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    # Reservations
    path('reserve/<slug:slug>/', views.ReserveBicycleView.as_view(), name='reserve'),
    path('reservation/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservation/active/', views.ActiveReservationView.as_view(), name='reservation-active'),
    path('reservation/<int:pk>/cancel/', views.CancelReservationView.as_view(), name='reservation-cancel'),
    path('reservation/<int:pk>/status/', views.CheckReservationStatusView.as_view(), name='reservation-status'),
    
    # Rentals
    path('start/<int:pk>/', views.StartRentalView.as_view(), name='start'),
    path('active/', views.ActiveRentalView.as_view(), name='active'),
    path('return/', views.RentalReturnView.as_view(), name='return'),
    path('history/', views.RentalHistoryView.as_view(), name='history'),
    path('<int:pk>/', views.RentalDetailView.as_view(), name='detail'),
]