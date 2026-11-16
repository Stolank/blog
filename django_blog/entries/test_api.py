import io
import json
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, City, Comment


class JournalApiTests(TestCase):
    def test_article_search_pagination_and_detail(self):
        published_at = timezone.now()
        Article.objects.create(title="Rails", content="Первый текст", published_at=published_at)
        expected = Article.objects.create(
            title="Django на Windows", content="Второй текст", published_at=published_at
        )
        Article.objects.create(title="Django на Mac", content="Третий текст", published_at=published_at)

        response = self.client.get(reverse("api:articles"), {"q": "django", "page": 2, "per": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["meta"], {"page": 2, "per": 1, "total": 2, "pages": 2})
        self.assertEqual([entry["id"] for entry in response.json()["data"]], [expected.pk])
        detail = self.client.get(reverse("api:article", args=[expected.pk])).json()["data"]
        self.assertEqual(detail["content"], "Второй текст")
        self.assertEqual(detail["title"], expected.title)

    def test_city_search_by_country_and_missing_detail(self):
        city = City.objects.create(name="Almaty", country="Kazakhstan", last_temp=0)
        other = City.objects.create(name="Berlin", country="Germany", last_temp=2)
        response = self.client.get(reverse("api:cities"), {"q": "KAZAKHSTAN"})
        self.assertEqual(response.json()["data"], [{"id": city.pk, "name": "Almaty", "country": "Kazakhstan"}])
        self.assertEqual(self.client.get(reverse("api:city", args=[city.pk])).json()["data"]["name"], "Almaty")
        missing = self.client.get(reverse("api:city", args=[other.pk + 1]))
        self.assertEqual(missing.status_code, 404)
        self.assertIn("error", missing.json())

    def test_pagination_handles_invalid_values_and_pages_outside_results(self):
        url = reverse("api:articles")
        response = self.client.get(url, {"page": "bad", "per": 1000}).json()
        self.assertEqual(response["meta"], {"page": 1, "per": 100, "total": 0, "pages": 0})
        response = self.client.get(url, {"page": 10**30, "per": -1}).json()
        self.assertEqual(response["data"], [])
        self.assertEqual(response["meta"]["per"], 1)

    def test_comments_are_nested_and_read_only(self):
        parent = Comment.objects.create(body="Начало обсуждения")
        child = Comment.objects.create(body="Ответ", parent=parent)
        url = reverse("api:comments")
        self.assertEqual(self.client.get(url).json(), {"data": [{
            "id": parent.pk,
            "body": parent.body,
            "children": [{"id": child.pk, "body": child.body, "children": []}],
        }]})
        self.assertEqual(self.client.post(url, {"body": "Новая запись"}).status_code, 405)
        self.assertEqual(Comment.objects.count(), 2)

    @patch.dict("os.environ", {"OPENWEATHER_KEY": ""})
    @patch("entries.weather.urlopen")
    def test_weather_demo_is_labelled_and_avoids_network(self, request_weather):
        params = {"city": "Кызылорда"}
        response = self.client.get(reverse("weather"), params)
        self.assertContains(response, "Кызылорда")
        self.assertContains(response, "Демонстрационные данные")
        api = self.client.get(reverse("api:weather"), params).json()
        self.assertEqual(api["город"], "Кызылорда")
        self.assertTrue(api["демо"])
        request_weather.assert_not_called()

    @patch.dict("os.environ", {"OPENWEATHER_KEY": "test-key"})
    @patch("entries.weather.urlopen")
    def test_weather_maps_live_response_and_encodes_query(self, request_weather):
        raw = {
            "name": "New York",
            "main": {"temp": -2, "feels_like": -5, "humidity": 60, "pressure": 1010},
            "weather": [{"description": "облачно"}],
            "wind": {"speed": 2.5},
        }
        request_weather.return_value = io.BytesIO(json.dumps(raw).encode("utf-8"))
        response = self.client.get(reverse("api:weather"), {"city": "New York,US"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["температура"], -2)
        self.assertEqual(response.json()["ветер"], "2.5 м/с")
        self.assertFalse(response.json()["демо"])
        url = urlsplit(request_weather.call_args.args[0])
        self.assertEqual(url.netloc, "api.openweathermap.org")
        self.assertEqual(parse_qs(url.query)["q"], ["New York,US"])
        self.assertEqual(request_weather.call_args.kwargs["timeout"], 5)

    @patch.dict("os.environ", {"OPENWEATHER_KEY": "test-key"})
    @patch("entries.weather.urlopen")
    def test_weather_errors_are_handled_without_echoing_the_key(self, request_weather):
        url = reverse("api:weather")
        self.assertEqual(self.client.get(url, {"city": "x" * 121}).status_code, 400)
        request_weather.assert_not_called()
        request_weather.side_effect = HTTPError("https://example.test", 404, "Not found", {}, None)
        self.assertEqual(self.client.get(url).status_code, 404)
        request_weather.side_effect = URLError("test-key in upstream error")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 502)
        self.assertNotContains(response, "test-key", status_code=502)
