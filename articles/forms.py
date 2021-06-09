from django import forms
from .models import Comment, Article
from django.contrib.auth.forms import UserChangeForm




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'slug']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'slug']

    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']

        if commit:
            blog_post.save()
        return blog_post


# class EditProfileForm(UserChangeForm):
#     email =
#
#     class Meta:
