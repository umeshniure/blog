from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'comment {} by {}'.format(self.body, self.name)