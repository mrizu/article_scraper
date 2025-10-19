from rest_framework.decorators import api_view
from rest_framework.response import Response
from scraper.models import Article
from scraper.serializers import ArticleSerializer


@api_view(["GET"])
def articles(request):
    source = request.GET.get("source")

    if source:
        articles = Article.objects.filter(domain__icontains=source)
    else:
        articles = Article.objects.all()

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return Response({"error": "Article not found"}, status=404)

    serializer = ArticleSerializer(article)
    return Response(serializer.data)
