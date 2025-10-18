from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=1000)
    html_content = models.TextField()
    text_content = models.TextField()
    url = models.URLField(unique=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"