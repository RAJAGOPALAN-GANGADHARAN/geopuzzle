from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from users.forms import AuthenticationForm, RegistrationForm


class LoginView(DefaultLoginView):
    form_class = AuthenticationForm


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(FormView):
    template_name = 'user/profile.html'