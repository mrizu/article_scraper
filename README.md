# Article Scraper

## How to install and use

### Run commands in terminal in \scraper:

```
pip install -r .\requirements.txt
```

```
playwright install
```

### Running server for the first time:

```
cd .\article_scraper\
```

```
docker-compose up -d
```

```
python .\manage.py makemigrations
```

```
python .\manage.py migrate
```

```
python .\manage.py runserver
```

### Using scraper command

in \management\commands\scrape_articles.py
add desired article urls to ARTICLE_URLS

```
python .\manage.py scrape_articles
```

### Available API endpoints:

**/articles** - list all articles in DB

**/articles/[article_id]** - get detailed information from article by id

**/articles/?source=[domain]** - get articles listed by domain
