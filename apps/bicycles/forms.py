from django import forms
from .models import Bicycle, MaintenanceLog
from apps.stations.models import Station


class BicycleForm(forms.ModelForm):
    """
    Form for adding/editing bicycles (Admin only)
    """
    class Meta:
        model = Bicycle
        fields = [
            'name', 'model', 'manufacturer', 'serial_number',
            'description', 'image', 'frame_size', 'color',
            'gear_count', 'hourly_rate', 'status', 'condition',
            'current_station', 'purchase_date', 'purchase_price'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'frame_size': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'gear_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'current_station': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class BicycleSearchForm(forms.Form):
    """
    Form for searching and filtering bicycles
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, model, or serial number...'
        })
    )
    
    station = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        required=False,
        empty_label="All Stations",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Bicycle.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    min_rate = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min rate',
            'step': '0.01'
        })
    )
    
    max_rate = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max rate',
            'step': '0.01'
        })
    )


class MaintenanceLogForm(forms.ModelForm):
    """
    Form for logging bicycle maintenance
    """
    class Meta:
        model = MaintenanceLog
        fields = ['bicycle', 'description', 'cost', 'performed_by', 'is_completed']
        widgets = {
            'bicycle': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'performed_by': forms.TextInput(attrs={'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }