from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.utils import timezone

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


def upload_location(instance, filename):
    file_path = f'blog/{instance.author.id}/{instance.title}-{filename}'.format(author_id=str(instance.author_id),
                                                                                title=str(instance.title),
                                                                                filename=filename)
    return file_path


class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_location)
    updated_on = models.DateTimeField(auto_now=True)
    # body = models.TextField()
    body = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


@receiver(post_delete, sender=Article)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


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
