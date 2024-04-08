from django import forms
from django.contrib.auth.models import User

class StudentLoginForm(forms.Form):
    username = forms.EmailField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'name@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=264)


class StudentRegisterForm(forms.ModelForm):

    username = forms.EmailField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'name@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=264)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=264)
    first_name = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=264,widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ("username","password","first_name","last_name",)