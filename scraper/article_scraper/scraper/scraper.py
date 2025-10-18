import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    print(soup.prettify())
    # metatags = soup.find_all("meta")
    # for tag in metatags:
    #     print(tag)


def scrape_title(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    title = soup.find("title")

    return title.get_text(strip=True)


def scrape_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_selector("div.article-content")

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        article_div = soup.find("div", class_="article-content")
        if article_div:
            return article_div.get_text(separator="\n", strip=True)
        else:
            return "Article not found"


def scrape_publish_time(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
