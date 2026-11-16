from django.views.generic import DetailView, ListView, TemplateView

from .models import Article


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_articles"] = Article.objects.published()[:3]
        return context


class ArticleListView(ListView):
    def get_queryset(self):
        return Article.objects.published()


class ArticleDetailView(DetailView):
    def get_queryset(self):
        return Article.objects.published()
