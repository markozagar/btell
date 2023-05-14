from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login

from django import forms
from django.urls import reverse_lazy

from django.shortcuts import redirect


class LoginPage(auth_views.LoginView):
    template_name = 'btell_main/accounts/login.html'
    form_class = auth_forms.AuthenticationForm
    success_url = reverse_lazy('btell_index')
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        del form._errors['__all__']  # type: ignore # it works, but shows an error
        form.add_error(None, "Please enter a correct username and password. Note that both fields are case-sensitive.")
        return super().form_invalid(form)  # type: ignore # it works, but shows an error

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, user)
        return redirect('btell_index')
