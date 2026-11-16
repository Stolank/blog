from django.db.models import Q
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_safe

from .models import Article, City, Comment
from .weather import weather_api


ARTICLE_FIELDS = ("id", "title", "content", "created_at")
CITY_FIELDS = ("id", "name", "country")


def positive_int(value, default):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def list_response(request, records):
    page = positive_int(request.GET.get("page"), 1)
    per = min(positive_int(request.GET.get("per"), 10), 100)
    total = records.count()
    offset = (page - 1) * per
    data = list(records[offset:offset + per]) if offset < total else []
    return JsonResponse({
        "data": data,
        "meta": {"page": page, "per": per, "total": total, "pages": (total + per - 1) // per},
    })


def detail_response(records, pk):
    record = records.filter(pk=pk).first()
    if record is None:
        return JsonResponse({"error": "Record not found"}, status=404)
    return JsonResponse({"data": record})


@require_safe
def articles(request):
    records = Article.objects.published()
    query = request.GET.get("q", "").strip()
    if query:
        records = records.filter(title__icontains=query)
    return list_response(request, records.values(*ARTICLE_FIELDS))


@require_safe
def article(request, pk):
    return detail_response(Article.objects.published().values(*ARTICLE_FIELDS), pk)


@require_safe
def cities(request):
    query = request.GET.get("q", "").strip()
    records = City.objects.filter(Q(name__icontains=query) | Q(country__icontains=query)) if query else City.objects.all()
    return list_response(request, records.values(*CITY_FIELDS))


@require_safe
def city(request, pk):
    return detail_response(City.objects.values(*CITY_FIELDS), pk)


@require_safe
def comments(request):
    rows = list(Comment.objects.values_list("pk", "body", "parent_id"))
    nodes = {pk: {"id": pk, "body": body, "children": []} for pk, body, _ in rows}
    roots = []
    for pk, _, parent_id in rows:
        if parent_id is None:
            roots.append(nodes[pk])
        else:
            nodes[parent_id]["children"].append(nodes[pk])
    return JsonResponse({"data": roots})


urlpatterns = [
    path("articles/", articles, name="articles"),
    path("articles/<int:pk>/", article, name="article"),
    path("cities/", cities, name="cities"),
    path("cities/<int:pk>/", city, name="city"),
    path("comments/", comments, name="comments"),
    path("weather/", weather_api, name="weather"),
]
