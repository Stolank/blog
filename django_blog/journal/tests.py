from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from entries.models import Article, City


User = get_user_model()


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class AccountsTests(TestCase):
    password = "Window-map-8407!"

    def register(self, *, follow=False, **changes):
        data = {
            "username": "Reader@Example.test",
            "password1": self.password,
            "password2": self.password,
        }
        return self.client.post(reverse("register"), data | changes, follow=follow)

    def test_registration_creates_reader_with_hashed_password(self):
        response = self.register(is_staff="True", is_superuser="True", follow=True)

        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Учётная запись создана")
        reader = User.objects.get(username="reader@example.test")
        self.assertEqual(reader.email, reader.username)
        self.assertTrue(reader.check_password(self.password))
        self.assertNotEqual(reader.password, self.password)
        self.assertFalse(reader.is_staff)
        self.assertFalse(reader.is_superuser)

    def test_registration_rejects_duplicate_email_and_invalid_form(self):
        self.register()
        duplicate = self.register(username="READER@example.test")
        invalid = self.register(username="not-an-email", password2="different")

        self.assertContains(duplicate, "Учётная запись с такой электронной почтой уже существует")
        self.assertIn("username", invalid.context["form"].errors)
        self.assertIn("password2", invalid.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)

    def test_reader_can_log_in_refresh_and_log_out(self):
        self.register()
        response = self.client.post(reverse("login"), {
            "username": "READER@example.test",
            "password": self.password,
        })

        self.assertRedirects(response, reverse("home"))
        self.assertContains(self.client.get(reverse("city_list")), "reader@example.test")
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_wrong_credentials_without_distinguishing_unknown_users(self):
        self.register()
        responses = [
            self.client.post(reverse("login"), {"username": email, "password": "invalid"})
            for email in ("reader@example.test", "unknown@example.test")
        ]

        self.assertEqual(responses[0].context["form"].non_field_errors(), responses[1].context["form"].non_field_errors())
        self.assertTrue(responses[0].context["form"].non_field_errors())
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_forms_require_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        for route in ("register", "login", "logout"):
            with self.subTest(route=route):
                self.assertEqual(client.post(reverse(route)).status_code, 403)

    def test_guest_and_reader_are_redirected_from_admin_pages(self):
        reader = User.objects.create_user(username="reader@example.test", password=self.password)
        pages = [reverse("admin:index"), reverse("admin:entries_article_add"), reverse("admin:entries_city_add")]

        for user in (None, reader):
            if user:
                self.client.force_login(user)
            self.assertContains(self.client.get(reverse("article_list")), "Статьи")
            for page in pages:
                with self.subTest(user=user, page=page):
                    expected = f"{reverse('admin:login')}?next={page}"
                    self.assertRedirects(self.client.get(page), expected)
                    self.assertRedirects(self.client.post(page), expected)
        self.assertFalse(Article.objects.exists())
        self.assertFalse(City.objects.exists())

    def test_staff_without_model_permission_cannot_create_article(self):
        staff = User.objects.create_user(username="staff", password=self.password, is_staff=True)
        self.client.force_login(staff)

        response = self.client.post(reverse("admin:entries_article_add"), {
            "title": "Статья без разрешения",
            "content": "Запись должна быть отклонена.",
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.exists())

    def test_article_saved_in_admin_is_visible_to_guests(self):
        editor = User.objects.create_superuser(username="editor", password=self.password)
        self.client.force_login(editor)
        title = "Первая прогулка"
        full_text = "Текст новой статьи.\n\nВторой абзац."

        self.assertRedirects(
            self.client.post(reverse("admin:entries_article_add"), {"title": title, "content": full_text}),
            reverse("admin:entries_article_changelist"),
        )
        article = Article.objects.get(title=title)
        detail_url = reverse("article_detail", args=[article.pk])
        edit_url = reverse("admin:entries_article_change", args=[article.pk])
        self.assertContains(self.client.get(edit_url), f'href="{detail_url}"')

        guest = Client()
        for page in ("home", "article_list"):
            self.assertContains(guest.get(reverse(page)), f'href="{detail_url}">{title}</a>')
        self.assertContains(guest.get(detail_url), "<p>Второй абзац.</p>")

    def test_administrator_can_create_edit_and_delete_both_kinds_of_entry(self):
        User.objects.create_superuser(username="editor", password=self.password)
        login = self.client.post(reverse("login"), {"username": "editor", "password": self.password})
        self.assertRedirects(login, reverse("home"))
        self.assertContains(self.client.get(reverse("home")), 'href="/admin/"')

        records = [
            (Article, {"title": "История", "content": "Первый текст"}, "title", "Новая история"),
            (City, {"name": "Кызылорда", "country": "Казахстан", "last_temp": 0}, "name", "Алматы"),
        ]
        for model, fields, name, edited in records:
            with self.subTest(model=model):
                route = f"admin:entries_{model._meta.model_name}"
                self.assertEqual(self.client.post(reverse(f"{route}_add"), fields).status_code, 302)
                entry = model.objects.get()
                change_url = reverse(f"{route}_change", args=[entry.pk])
                self.assertEqual(self.client.post(change_url, fields | {name: edited}).status_code, 302)
                entry.refresh_from_db()
                self.assertEqual(getattr(entry, name), edited)
                delete_url = reverse(f"{route}_delete", args=[entry.pk])
                self.assertEqual(self.client.post(delete_url, {"post": "yes"}).status_code, 302)
                self.assertFalse(model.objects.filter(pk=entry.pk).exists())
