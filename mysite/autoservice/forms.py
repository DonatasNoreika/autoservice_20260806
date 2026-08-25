from django import forms
from django.contrib.auth.models import User
from .models import OrderComment, Profile, Order

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ['content']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'deadline', 'status']
        widgets = {"deadline": forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')}

