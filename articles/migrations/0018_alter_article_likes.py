# Generated by Django 3.2.5 on 2021-09-24 17:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0017_alter_article_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
