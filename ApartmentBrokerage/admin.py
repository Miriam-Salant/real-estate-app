from django.contrib import admin
from . import models

admin.site.register(models.Users)
admin.site.register(models.Apartment)
admin.site.register(models.Message)
admin.site.register(models.ApartmentImage)

