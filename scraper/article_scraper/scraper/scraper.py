import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_html(url, headers):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    print(soup.prettify())
    metatags = soup.find_all("meta")
    for tag in metatags:
        print(tag)


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

    return published_time
