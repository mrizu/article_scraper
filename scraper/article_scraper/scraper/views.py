from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .scraper import scrape_title, scrape_article_content, scrape_publish_time
from .parsers import normalize_iso_date, extract_domain


# Create your views here.
def home(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    # url = "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa"
    # url = "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow"
    url = "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie"
    try:
        title = scrape_title(url, headers).get_text(strip=True)
        article_content = scrape_article_content(url).get_text()
        published_time = normalize_iso_date(scrape_publish_time(url, headers))
        domain = extract_domain(url)
        return JsonResponse(
            {
                "title": title,
                "published_at": published_time,
                "domain": domain,
                "article-content": article_content,
            },
            json_dumps_params={"ensure_ascii": False},
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
