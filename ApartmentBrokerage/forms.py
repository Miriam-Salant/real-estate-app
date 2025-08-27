from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Apartment, ApartmentImage


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = Users
        fields = ['username', 'password1', 'password2', 'phone', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        return user


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['city', 'neighborhood', 'street', 'price', 'rooms', 'floor', 'description', 'isBrokerage']


class ImagesForm(forms.ModelForm):
    class Meta:
        model = ApartmentImage
        fields = ['image']

    # image = forms.ImageField(
    #     widget=forms.FileInput(attrs={'multiple': True}),  # Use FileInput instead of ClearableFileInput
    #     required=False  # Make it optional
    # )
