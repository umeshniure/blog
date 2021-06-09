from django.contrib import admin
from .models import Article
from .models import Article, Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'status', 'created_on', 'image')
    list_filter = ('status',)
    search_fields = ('title', 'body', 'author')
    actions = ['publish']

    def publish(self, request, queryset):
        queryset.update(status=True)


admin.site.register(Article, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
