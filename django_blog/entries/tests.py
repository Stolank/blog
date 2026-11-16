from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Article, City


class PublicPagesTests(TestCase):
    def test_home_links_to_both_sections(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'href="/articles/"')
        self.assertContains(response, 'href="/cities/"')

    def test_lists_show_empty_state(self):
        self.assertContains(self.client.get(reverse("article_list")), "Статей пока нет.")
        self.assertContains(self.client.get(reverse("city_list")), "Городов пока нет.")

    def test_home_shows_three_most_recent_articles(self):
        articles = [Article.objects.create(title=f"Заметка {number}", content="Текст") for number in range(4)]
        response = self.client.get(reverse("home"))

        self.assertEqual(list(response.context["recent_articles"]), list(reversed(articles[1:])))
        self.assertContains(response, reverse("article_detail", args=[articles[-1].pk]))

    def test_article_list_links_to_full_text_with_escaped_markup(self):
        article = Article.objects.create(title="История города", content="<script>example</script>\n\nВторой абзац")
        detail_url = reverse("article_detail", args=[article.pk])

        self.assertContains(self.client.get(reverse("article_list")), f'href="{detail_url}"')
        response = self.client.get(detail_url)
        self.assertContains(response, "&lt;script&gt;example&lt;/script&gt;")
        self.assertContains(response, "<p>Второй абзац</p>")
        self.assertNotContains(response, "<script>")

    def test_city_list_links_to_country_and_saved_temperature(self):
        city = City.objects.create(name="Кызылорда", country="Казахстан", last_temp=0)
        detail_url = reverse("city_detail", args=[city.pk])

        self.assertContains(self.client.get(reverse("city_list")), f'href="{detail_url}"')
        response = self.client.get(detail_url)
        self.assertContains(response, "Кызылорда")
        self.assertContains(response, "Казахстан")
        self.assertContains(response, "0,0&nbsp;°C")

    @override_settings(DEBUG=False)
    def test_missing_pages_show_journal_not_found_page(self):
        paths = [
            reverse("article_detail", args=[999]),
            reverse("city_detail", args=[999]),
            "/missing/",
        ]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, "Страница не найдена", status_code=404)
                self.assertContains(response, 'href="/articles/">Все статьи</a>', status_code=404)

    def test_rails_list_addresses_redirect_to_django_lists(self):
        self.assertRedirects(self.client.get("/articles"), reverse("article_list"), status_code=301)
        self.assertRedirects(self.client.get("/cities"), reverse("city_list"), status_code=301)
