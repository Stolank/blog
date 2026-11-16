from django.urls import path
from django.views.generic import DetailView, ListView

from .models import Article, City
from .views import HomeView
from .weather import weather_page


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ListView.as_view(model=Article), name="article_list"),
    path("articles/<int:pk>/", DetailView.as_view(model=Article), name="article_detail"),
    path("cities/", ListView.as_view(model=City), name="city_list"),
    path("cities/<int:pk>/", DetailView.as_view(model=City), name="city_detail"),
    path("weather/", weather_page, name="weather"),
]
