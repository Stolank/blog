from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


USERNAME_LIMIT = get_user_model()._meta.get_field("username").max_length
DUPLICATE_EMAIL = "Учётная запись с такой электронной почтой уже существует."


class RegistrationForm(UserCreationForm):
    username = forms.EmailField(
        label="Электронная почта",
        max_length=USERNAME_LIMIT,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        if self._meta.model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(DUPLICATE_EMAIL)
        return username

    def save(self, commit=True):
        self.instance.email = self.cleaned_data["username"]
        return super().save(commit=commit)


class JournalLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Электронная почта или имя пользователя",
        max_length=USERNAME_LIMIT,
        widget=forms.TextInput(attrs={"autocomplete": "username", "autocapitalize": "none"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if "@" in username:
            return username.lower()
        return username


class RegistrationView(CreateView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                response = super().form_valid(form)
        except IntegrityError:
            if not get_user_model().objects.filter(username=form.cleaned_data["username"]).exists():
                raise
            form.add_error("username", DUPLICATE_EMAIL)
            return self.form_invalid(form)
        messages.success(self.request, "Учётная запись создана. Теперь можно войти.")
        return response
