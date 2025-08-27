from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('apartments/', views.apartment_list, name='apartments'),
    path('seller_appartments/', views.seller_appartments, name='seller_appartments'),
    path('add_message/<int:apartment_id>/', views.add_message, name='add_message'),
    path('submit_message/<int:apartment_id>/', views.submit_message, name='submit_message'),
    path('add_apartment/', views.add_apartment, name='add_apartment'),
    path('sell-apartment/<int:apartmentId>/', views.sell_apartment, name='sell_apartment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)