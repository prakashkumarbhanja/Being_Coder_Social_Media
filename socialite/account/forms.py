from django.contrib.auth.models import User
from django import forms

class Create_User_Form(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'password', 'confirm_password')
