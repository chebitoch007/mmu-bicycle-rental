from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, CustomPasswordResetForm
from .models import User


class UserRegistrationView(CreateView):
    """
    User registration view for students and staff
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registration successful! Please wait for admin verification before logging in.'
        )
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register - MMU Bicycle Rental'
        return context


class UserLoginView(LoginView):
    """
    Custom login view with university ID support
    """
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Check if user is verified
        if not user.is_verified:
            messages.error(
                self.request,
                'Your account is pending verification by admin. Please wait for approval.'
            )
            return redirect('accounts:login')
        
        messages.success(self.request, f'Welcome back, {user.get_full_name()}!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login - MMU Bicycle Rental'
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    View user profile
    """
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Profile'
        context['total_rentals'] = self.request.user.get_total_rentals()
        context['active_rental'] = self.request.user.rentals.filter(status='active').first()
        context['recent_rentals'] = self.request.user.rentals.filter(
            status='completed'
        ).order_by('-end_time')[:5]
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update user profile
    """
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile'
        return context


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view
    """
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'emails/password_reset_email.html'
    subject_template_name = 'emails/password_reset_subject.txt'
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Password reset instructions have been sent to your email.'
        )
        return super().form_valid(form)