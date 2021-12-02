from django import forms
from .models import Comment, Article, Categories
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm

choices = Categories.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'body', 'image', 'slug']
        # fields = '__all__'
        widgets = {
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'category', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def save(self, commit=True):
            blog_post = self.instance
            blog_post.title = self.cleaned_data['title']
            blog_post.body = self.cleaned_data['body']
            blog_post.slug = self.cleaned_data['slug']
            blog_post.category = self.cleaned_data['category']

            if self.cleaned_data['image']:
                blog_post.image = self.cleaned_data['image']

            if commit:
                blog_post.save()
            return blog_post
