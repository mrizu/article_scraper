import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
from scraper.models import Article
from .parsers import normalize_iso_date, extract_domain


def scrape_title(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.find("title")

    if title:
        return title
    else:
        return "Title not found"


def scrape_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        if page.is_visible("div.article-content"):
            page.wait_for_selector("div.article-content")
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            article_div = soup.find("div", class_="article-content")
        else:
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            article_div = soup.find(
                "div", class_="post-text-two-red table-post mt-8 quote-red link-red"
            )

        if article_div:
            return article_div
        else:
            return "Article content not found"


def scrape_publish_time(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    published_time = soup.find("meta", attrs={"property": "article:published_time"})

    if not published_time:
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for entry in data:
                        if "datePublished" in entry:
                            return entry["datePublished"]
                elif "datePublished" in data:
                    return data["datePublished"]
            except Exception:
                continue

    return published_time.get("content") if published_time else "Publish time not found"


def scrape_article(url):
    if Article.objects.filter(url=url).exists():
        print(f"Article already exists in DB: {url}")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    title = scrape_title(url, headers).get_text(strip=True)
    html_content = scrape_article_content(url).get_text()
    text_content = scrape_article_content(url).get_text(separator="\n", strip=True)
    published_time = normalize_iso_date(scrape_publish_time(url, headers))
    domain = extract_domain(url)

    article = Article.objects.create(
        title=title,
        html_content=html_content,
        text_content=text_content,
        url=url,
        domain=domain,
        published_at=published_time,
    )

    print(f"Saved article: {url}")
    return article
