pip install -r .\requirements.txt
playwright install
cd .\article_scraper\
docker-compose up -d
python .\manage.py makemigrations
python .\manage.py migrate
python .\manage.py runserver
python .\manage.py scrape_articles
