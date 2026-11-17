from django import template

register = template.Library()

ISSUE_ARTWORK = {
    "Добро пожаловать в OldSchool Journal": {
        "icon": "journal/first-issue/icon-welcome.png",
        "thumb": "journal/first-issue/welcome-thumb.webp",
        "summary": "О чём наш журнал, почему мы пишем об Алматы и какие истории ждут на этих страницах.",
    },
    "Алматы с блокнотом": {
        "icon": "journal/first-issue/icon-walk.png",
        "thumb": "journal/first-issue/walk-thumb.webp",
        "banner": "journal/first-issue/walk-banner.webp",
        "summary": "Знакомые маршруты, заметки на ходу и маленькие открытия во время прогулки по Алматы.",
    },
    "Как читать страницу «Погода»": {
        "icon": "journal/first-issue/icon-weather.png",
        "thumb": "journal/first-issue/weather-thumb.webp",
        "summary": "Как найти город и отличить текущую погоду от демонстрационных данных.",
    },
}


@register.simple_tag
def issue_artwork(article):
    return ISSUE_ARTWORK.get(article.title, {})
