# from btell_main.models import Profile
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login
# from django.contrib.auth import views as auth_views
from django.contrib.auth import models as auth_models
from django.contrib.auth import forms as auth_forms

# from datetime import datetime, timezone


class Register_User(auth_forms.UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    accepted_cookies = forms.BooleanField(required=True, label='Cookies')
    accepted_tos = forms.BooleanField(required=True, label='ToS')

    class Meta:
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

        u1 = ""
        if 'username' in data:
            u1 = str(data['username'])

        if u1 != "":
            if len(u1) > 100:  # TODO Decide max username lenght
                self.add_error('username', "The name is too long. Max 100 marks.")

            u_check = auth_models.User.objects.filter(username=u1)
            if u_check.exists():
                self.add_error('username', "Such Player already exists.")

        e1 = ""
        if 'email' in data:
            e1 = data['email']

        if e1 != "":
            if validate_email(e1) is not None:
                self.add_error('email', "It's not in e-mail format.")

            if len(e1) > 100:  # TODO Decide max e-mail lenght
                self.add_error('email', "E-mail is too long. Max 100 marks.")

            e_check = auth_models.User.objects.filter(email=e1)  # TODO If you want it
            if e_check.exists():
                self.add_error('email', "Email is already assigned to some account.")

        p1 = ""
        if 'password1' in data:
            p1 = data['password1']

        # if p1 != "":  # TODO Pick any password requirements you want
        #     if len(p1) > 50:
        #         self.add_error('password1', "The password is too long. Max 50 marks.")

        #     if len(p1) < 8:
        #         self.add_error('password1', "The password is too short.")

        #     if not any(letter.isupper() for letter in p1):
        #         self.add_error('password1', "The password needs an uppercase.")

        #     if not any(letter.islower() for letter in p1):
        #         self.add_error('password1', "The password needs a lowercase.")

        #     if not any(letter.isdecimal() for letter in p1):
        #         self.add_error('password1', "The password needs a number.")

        #     if not any(not letter.isalnum() for letter in p1):
        #         self.add_error('password1', "The password needs a special mark.")

        # p2 = ""  # Solved by Django
        # if 'password2' in data:
        #     p2 = str(data['password2'])

        # if p1 != p2:  # Solved by Django
        #     self.add_error('password2', "Passwords are not identical.")

        cook = False
        print(f"cookies is = {cook}")
        if 'accepted_cookies' in data:
            cook = data['accepted_cookies']
            # cook = True

        if cook is not True:
            print(f"cookies is = {cook}")
            self.add_error('accepted_cookies', "Cookies Policy not accepted.")

        tos = False
        print(f"tos is = {tos}")
        if 'accepted_tos' in data:
            tos = data['accepted_tos']
            # tos = True

        if tos is not True:
            print(f"tos is = {tos}")
            self.add_error('accepted_tos', "Terms of Use not accepted.")

        return data

    # def save(self, commit=True):
    #     user = super(Register_User, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.tos = self.cleaned_data['accepted_tos']
    #     user.cookies = self.cleaned_data['accepted_cookies']
    #     if commit:
    #         user.save()
    #     return user


class RegisterPage(FormView):
    template_name = 'btell_main/accounts/registration.html'
    form_class = Register_User
    redirect_authenticated_user = True
    success_url = reverse_lazy('btell_index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('btell_index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        # Registration
        user = form.save()  # type: ignore # it works, but shows an error

        # Profile manipulation if any should be here, or in the models

        # Logging
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return redirect('btell_index')
