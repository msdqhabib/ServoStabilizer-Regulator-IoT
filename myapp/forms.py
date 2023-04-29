from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class NewuserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class meta:
        models = User
        fields = ["username","email","password1","password2"]


    def save(self, commit=True):
        user = super(NewuserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        return user