from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to admin users only
    """
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('home')


class VerifiedUserRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to verified users only
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_verified
    
    def handle_no_permission(self):
        messages.warning(self.request, 'Your account needs to be verified by an admin first.')
        return redirect('home')


class ActiveRenterRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access to users who can rent
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_rent
    
    def handle_no_permission(self):
        messages.error(self.request, 'You are not currently eligible to rent bicycles.')
        return redirect('bicycles:list')