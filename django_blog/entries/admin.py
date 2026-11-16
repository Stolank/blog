from django.contrib import admin

from .models import Article, City


admin.site.site_header = "Управление OldSchool Journal"
admin.site.site_title = "OldSchool Journal"
admin.site.index_title = "Управление журналом"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    search_fields = ("title", "content")

    def view_on_site(self, obj):
        return obj.get_absolute_url()


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "last_temp")
    search_fields = ("name", "country")
