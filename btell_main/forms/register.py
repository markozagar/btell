"""Registration form and view."""
import logging

from django import shortcuts, urls, forms, http
from django.core import validators
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth import models as auth_models
from django.contrib.auth import forms as auth_forms
from django.views.generic import edit

from btell import settings


class RegisterUser(auth_forms.UserCreationForm):
    """Registration form."""
    email = forms.EmailField(required=True, label='Email')
    accepted_cookies = forms.BooleanField(required=True, label='Cookies')
    accepted_tos = forms.BooleanField(required=True, label='ToS')

    class Meta:  # pylint:disable=missing-class-docstring,too-few-public-methods
        model = auth_models.User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'accepted_cookies',
            'accepted_tos',
        )

    def clean(self):
        data = self.cleaned_data

        provided_username = ""
        if 'username' in data:
            provided_username = str(data['username'])

        if provided_username != "":
            if len(provided_username) > settings.BTELL_MAX_USERNAME_LENGTH:
                self.add_error('username', "The name is too long. Max 100 marks.")

            u_check = auth_models.User.objects.filter(username=provided_username)
            if u_check.exists():
                self.add_error('username', "Such Player already exists.")

        provided_email = ""
        if 'email' in data:
            provided_email = data['email']

        if provided_email != "":
            if validators.validate_email(provided_email) is not None:
                self.add_error('email', "It's not in e-mail format.")

            e_check = auth_models.User.objects.filter(email=provided_email)
            if e_check.exists():
                self.add_error('email', "Email is already assigned to some account.")

        provided_password = ""
        if 'password1' in data:
            provided_password = data['password1']

        if password_validation.validate_password(provided_password):  # Will use password validation as configured in settings.py
            self.add_error('password1', "The given password is not secure enough.")
            password_hints = password_validation.password_validators_help_texts()
            for hint in password_hints:
                self.add_error('password1', hint)

        return data


class RegisterPage(edit.FormView):
    """Registration page."""
    template_name = 'btell_main/accounts/registration.html'
    form_class = RegisterUser
    redirect_authenticated_user = True
    success_url = urls.reverse_lazy('btell_index')

    def get(self, request, *args, **kwargs) -> http.HttpResponse:
        if self.request.user.is_authenticated:
            return shortcuts.redirect('btell_index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponse:
        form.save()

        # Automatically log the user in while we're at it.
        user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if isinstance(user, auth_models.User):
            auth.login(self.request, user)
        else:
            logging.error("Incorrect User model: %s (or the user was not correctly registered)", type(user))
        return shortcuts.redirect('btell_index')
