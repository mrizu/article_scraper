import logging
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
from scraper.models import Article
from .parsers import normalize_iso_date, extract_domain
from django.db import DatabaseError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def scrape_title(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("title")
    if not title_tag:
        logger.warning(f"Title not found for {url}")
        return None
    return title_tag.get_text(strip=True)


def scrape_article_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            article_div = soup.find("div", class_="article-content") or soup.find(
                "div", class_="post-text-two-red table-post mt-8 quote-red link-red"
            )

            browser.close()

            if article_div:
                return article_div
            else:
                logger.warning(f"Article content not found for {url}")
                return None
    except Exception as e:
        logger.error(f"Error loading {url} with Playwright: {e}")
        return None


def scrape_publish_time(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch publish time for {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    try:
        published_time = soup.find("meta", attrs={"property": "article:published_time"})
        if published_time:
            return published_time.get("content")

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
            except json.JSONDecodeError:
                continue

    except Exception as e:
        logger.warning(f"Could not parse publish time for {url}: {e}")

    logger.warning(f"Publish time not found for {url}")
    return None


def scrape_article(url):
    if Article.objects.filter(url=url).exists():
        logger.info(f"Article already exists in DB: {url}")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    try:
        title = scrape_title(url, headers)
        article_content = scrape_article_content(url)
        published_time_raw = scrape_publish_time(url, headers)
        published_time = (
            normalize_iso_date(published_time_raw) if published_time_raw else None
        )
        domain = extract_domain(url)

        if not (title and article_content and published_time):
            logger.warning(f"Skipping {url}: missing critical data")
            return None

        html_content = str(article_content)
        text_content = article_content.get_text(separator="\n", strip=True)

        try:
            article = Article.objects.create(
                title=title,
                html_content=html_content,
                text_content=text_content,
                url=url,
                domain=domain,
                published_at=published_time,
            )
            logger.info(f"Saved article: {url}")
            return article
        except DatabaseError as e:
            logger.error(f"Database error saving {url}: {e}")
            return None

    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {e}")
        return None
