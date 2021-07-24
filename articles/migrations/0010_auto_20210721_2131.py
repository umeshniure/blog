# Generated by Django 3.1.7 on 2021-07-21 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0009_auto_20210721_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(default=None, null=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
