import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe


class WeatherForm(forms.Form):
    city = forms.CharField(label="Город", max_length=120, required=False)


class WeatherError(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status


def fetch_weather(city):
    key = os.environ.get("OPENWEATHER_KEY", "").strip()
    if not key:
        return {
            "город": city,
            "температура": 22.0,
            "погода": "Пример погодных данных",
            "демо": True,
        }

    query = urlencode({"q": city, "appid": key, "units": "metric", "lang": "ru"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{query}", timeout=5) as response:
            data = json.load(response)
        return {
            "город": data["name"],
            "температура": data["main"]["temp"],
            "ощущается_как": data["main"]["feels_like"],
            "погода": data["weather"][0]["description"],
            "ветер": f"{data['wind']['speed']} м/с",
            "влажность": f"{data['main']['humidity']}%",
            "давление": f"{data['main']['pressure']} гПа",
            "демо": False,
        }
    except HTTPError as error:
        if error.code == 404:
            raise WeatherError("Город не найден. Проверьте название.", 404) from None
        raise WeatherError("Сервис погоды не ответил. Попробуйте позже.", 502) from None
    except (URLError, OSError, ValueError, KeyError, IndexError, TypeError):
        raise WeatherError("Не удалось получить данные о погоде. Попробуйте позже.", 502) from None


@require_safe
def weather_page(request):
    form = WeatherForm(request.GET if "city" in request.GET else {"city": "Almaty"})
    context = {"form": form}
    if not form.is_valid():
        return render(request, "weather.html", context, status=400)
    try:
        context["weather"] = fetch_weather(form.cleaned_data["city"] or "Almaty")
    except WeatherError as error:
        context["error"] = str(error)
        return render(request, "weather.html", context, status=error.status)
    return render(request, "weather.html", context)


@require_safe
def weather_api(request):
    form = WeatherForm(request.GET)
    if not form.is_valid():
        return JsonResponse({"ошибка": str(form.errors["city"][0]), "код": 400}, status=400)
    try:
        return JsonResponse(fetch_weather(form.cleaned_data["city"] or "Almaty"))
    except WeatherError as error:
        return JsonResponse({"ошибка": str(error), "код": error.status}, status=error.status)
