from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    published_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Article
        fields = "__all__"
