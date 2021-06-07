from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'slug']
