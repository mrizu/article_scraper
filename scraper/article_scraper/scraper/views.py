from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .scraper import scrape_title, scrape_article_content, get_html


# Create your views here.
def home(request):
    url = "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa"
    try:
        # title = scrape_title(url)
        # return JsonResponse({"title": title}, json_dumps_params={"ensure_ascii": False})
        article_content = scrape_article_content(url)
        get_html(url)
        return JsonResponse(
            {"article-content": article_content},
            json_dumps_params={"ensure_ascii": False},
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
