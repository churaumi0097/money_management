from django.shortcuts import render
from . import forms
from . import models
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate,login


class SignUpView(CreateView):
    model = models.CustomUser
    form_class = forms.CustomUserCreationForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        response = super().form_valid(form)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LoginView(LoginView):
    model = models.CustomUser
    form_class = forms.CustomLoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy("list")


class LogoutView(LogoutView):
    template_name = "account/logout.html"