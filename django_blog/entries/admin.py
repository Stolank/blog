from django.contrib import admin
from django.utils import timezone

from .models import Article, City


admin.site.site_header = "Управление OldSchool Journal"
admin.site.site_title = "OldSchool Journal"
admin.site.index_title = "Управление журналом"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_status", "published_at", "updated_at")
    readonly_fields = ("publication_status", "published_at")
    search_fields = ("title", "content")
    actions = ("publish_articles",)

    @admin.display(description="Статус")
    def publication_status(self, obj):
        return "Опубликовано" if obj and obj.published_at else "Черновик"

    @admin.action(permissions=["change"], description="Опубликовать выбранные статьи")
    def publish_articles(self, request, queryset):
        published_at = timezone.now()
        count = queryset.filter(published_at__isnull=True).update(
            published_at=published_at, updated_at=published_at
        )
        self.message_user(request, f"Опубликовано статей: {count}.")

    def save_model(self, request, obj, form, change):
        if change:
            # A concurrent publication must survive saving the edit form.
            obj.save(update_fields=("title", "content", "updated_at"))
        else:
            super().save_model(request, obj, form, change)

    def view_on_site(self, obj):
        if obj.published_at is not None:
            return obj.get_absolute_url()


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "last_temp")
    search_fields = ("name", "country")
