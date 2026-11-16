from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from .accounts import JournalLoginForm, RegistrationView


urlpatterns = [
    path("api/v1/", include(("entries.api", "api"))),
    path("users/sign_up/", RegistrationView.as_view(), name="register"),
    path("users/sign_in/", LoginView.as_view(authentication_form=JournalLoginForm), name="login"),
    path("users/sign_out/", LogoutView.as_view(), name="logout"),
    path("login", RedirectView.as_view(pattern_name="login")),
    path("admin/dashboard/", RedirectView.as_view(pattern_name="admin:index")),
    path("admin/", admin.site.urls),
    path("", include("entries.urls")),
]
