from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.PasswordInput()

    # last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # is_superuser = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # is_staff = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # is_active = forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    # date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
