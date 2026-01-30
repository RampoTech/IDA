from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, TemplateView, RedirectView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, resolve_url
from .models import User
from .forms import CustomUserCreationForm
from django.conf import settings

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

class AdminUserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/create_user.html'
    success_url = reverse_lazy('ticket_list') # Redirect to tickets after creation

    def test_func(self):
        return self.request.user.role == User.Role.ADMIN or self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect to home or show error
        return render(self.request, '403.html', status=403)

class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('ticket_list')

def logout_view(request):
    logout(request)
    return redirect('login')
