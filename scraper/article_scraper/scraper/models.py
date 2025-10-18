from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=400)
    html_content = models.TextField()
    text_content = models.TextField()
    url = models.URLField()
    domain = models.CharField(max_length=200)
    published_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
