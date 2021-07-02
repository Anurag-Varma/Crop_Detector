from django import forms
from .models import Image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image_name", "images", "longitude","latitude")

        widgets={
            'image_name':forms.TextInput(attrs={'class':'form-control'}),
            'longitude':forms.TextInput(attrs={'class':'form-control', 'readonly':True,'id':'longitude'}),
            'latitude':forms.TextInput(attrs={'class':'form-control',  'readonly':True,'id':'latitude'}),

        }

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['images'].required = True

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username","email","password1","password2")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-Enter password'
