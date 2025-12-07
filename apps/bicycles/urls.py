from django.urls import path
from . import views

app_name = 'bicycles'

urlpatterns = [
    # Bicycle CRUD
    path('', views.BicycleListView.as_view(), name='list'),
    path('add/', views.BicycleCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.BicycleDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.BicycleUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.BicycleDeleteView.as_view(), name='delete'),
    
    # Maintenance
    path('maintenance/log/', views.MaintenanceLogCreateView.as_view(), name='maintenance-log'),
]