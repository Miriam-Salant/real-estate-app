from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    seller = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group', related_name='person_set', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='person_set', blank=True)


class Apartment(models.Model):
    city = models.CharField(max_length=20, validators=[MinLengthValidator(2)])
    neighborhood = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    street = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(20000000)], null=True,
                                blank=True)
    rooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    floor = models.IntegerField(validators=[MinValueValidator(-10), MaxValueValidator(100)], null=True, blank=True)
    description = models.TextField(validators=[MinLengthValidator(2)], null=True, blank=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    isSold = models.BooleanField(default=False)
    isBrokerage = models.BooleanField(default=False)
    commission = models.IntegerField(default=0)


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')


class Message(models.Model):
    sender = models.ForeignKey(Users, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Users, related_name='received_messages', on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
