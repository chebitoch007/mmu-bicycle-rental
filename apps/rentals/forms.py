from django import forms
from .models import Rental
from apps.stations.models import Station


class RentalReturnForm(forms.Form):
    """
    Form for returning a rented bicycle
    """
    return_station = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Return Station"
    )
    
    return_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any issues or notes about the bicycle condition?'
        }),
        label="Return Notes"
    )
    
    distance_km = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Distance traveled (optional)'
        }),
        label="Distance (KM)"
    )
    
    damage_fee = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Damage fee if applicable'
        }),
        label="Damage Fee (KES)"
    )


class AdminRentalOverrideForm(forms.ModelForm):
    """
    Form for admin to override or manage rentals
    """
    class Meta:
        model = Rental
        fields = ['status', 'return_station', 'return_notes', 'damage_fee', 'late_fee']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'return_station': forms.Select(attrs={'class': 'form-select'}),
            'return_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'damage_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'late_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class RentalFilterForm(forms.Form):
    """
    Form for filtering rental history
    """
    status = forms.ChoiceField(
        choices=[('', 'All')] + Rental.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )