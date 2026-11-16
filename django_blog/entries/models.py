from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField("заголовок", max_length=255)
    content = models.TextField("текст")
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("обновлено", auto_now=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "статья"
        verbose_name_plural = "статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.pk])


class City(models.Model):
    name = models.CharField("название", max_length=255)
    country = models.CharField("страна", max_length=255)
    last_temp = models.FloatField("последняя температура, °C")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "country", "pk"]
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at", "pk"]
