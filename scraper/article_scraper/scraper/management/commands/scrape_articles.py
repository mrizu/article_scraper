from django.core.management.base import BaseCommand
from scraper.scraper import scrape_article

ARTICLE_URLS = [
    "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie",
    "https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu",
    "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa",
    "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow",
]


class Command(BaseCommand):
    help = "Scrape articles and save them to the database"

    def handle(self, *args, **options):
        total = len(ARTICLE_URLS)

        for i, url in enumerate(ARTICLE_URLS, start=1):
            self.stdout.write(f"Scraping article {i}/{total}: {url}")
            article = scrape_article(url)
            if article:
                self.stdout.write(self.style.SUCCESS(f"Article saved successfully."))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Skipped (url already exists): {url}")
                )

        self.stdout.write(self.style.SUCCESS("Scraping completed!"))
