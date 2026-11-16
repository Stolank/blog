from django.urls import path
from django.views.generic import DetailView, ListView, TemplateView

from .models import Article, City


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("articles/", ListView.as_view(model=Article), name="article_list"),
    path("articles/<int:pk>/", DetailView.as_view(model=Article), name="article_detail"),
    path("cities/", ListView.as_view(model=City), name="city_list"),
    path("cities/<int:pk>/", DetailView.as_view(model=City), name="city_detail"),
]
