from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    customuser_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)


    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone', 'customuser_group', 'password1', 'password2')


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'phone']  

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio'] 
