from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .models import Apartment, Message, Users, ApartmentImage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ApartmentForm, ImagesForm
from django.http import HttpResponseForbidden
from django.db import transaction


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'auth/register.html', {'form': form, 'submitted': True})
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/apartments')  # Redirect to homepage or another page
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def apartment_list(request):
    apartments = Apartment.objects.filter(isSold=False)

    city_filter = request.GET.get('city', None)
    rooms_filter = request.GET.get('rooms', None)

    if city_filter:
        apartments = apartments.filter(city__icontains=city_filter)

    if rooms_filter:
        apartments = apartments.filter(rooms=rooms_filter)
    return render(request, 'apartments.html', {'apartments': apartments})


@login_required
def seller_appartments(request):
    apartments = Apartment.objects.filter(owner=request.user)
    apartments_with_messages = [
        {
            'apartment': apartment,
            'messages': Message.objects.filter(apartment=apartment)
        }
        for apartment in apartments
    ]
    return render(request, 'sellerApartments.html', {
        'apartments_with_messages': apartments_with_messages
    })


@login_required
def seller_apartments(request):
    if not request.user.is_authenticated or not request.user.seller:
        return redirect('login')  # נוודא שהמשתמש מחובר ומוכר

    if request.method == "POST":
        message_id = request.POST.get("message_id")
        if message_id:
            try:
                message = Message.objects.get(id=message_id, receiver=request.user)
                message.read = True
                message.save()
            except Message.DoesNotExist:
                pass

    apartments = Apartment.objects.filter(owner=request.user)
    apartments_with_messages = [
        {
            "apartment": apartment,
            "messages": Message.objects.filter(apartment=apartment)
        }
        for apartment in apartments
    ]
    return render(request, 'sellerApartments.html', {
        'apartments_with_messages': apartments_with_messages
    })


@login_required
def add_message(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text:
            sender = request.user
            message = Message(sender=sender, receiver=apartment.owner, apartment=apartment, message=message_text)
            message.save()

        return redirect('submit_message', apartment_id=apartment.id)
    return render(request, 'addMessage.html', {'apartment': apartment})


@login_required
def submit_message(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    return render(request, 'submitMessage.html', {'apartment': apartment})


# @login_required
# def add_apartment(request):
#     if not request.user.seller:
#         return HttpResponseForbidden("אין לך הרשאה להוסיף דירה")
#
#     if request.method == 'POST':
#         form = ApartmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             apartment = form.save(commit=False)
#             apartment.owner = request.user
#             apartment.save()
#             if ApartmentImage.is_valid() and request.FILES.getlist('image'):
#                 for img in request.FILES.getlist('image'):
#                     ApartmentImage.objects.create(apartment=apartment, image=img)
#                     return redirect('apartments')
#
#             else:
#                 form = ApartmentForm()
#                 return render(request, 'addApartment.html', {'form': form})
#
# def add_apartment(request):
#     if not request.user.seller:
#         return HttpResponseForbidden("אין לך הרשאה להוסיף דירה")  # Forbidden for non-sellers
#
#     if request.method == 'POST':
#         form = ApartmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             apartment = form.save(commit=False)
#             apartment.owner = request.user
#             apartment.save()
#
#             # Handle images
#             images = request.FILES.getlist('image')
#             if images:  # Ensure images are present
#                 for img in images:
#                     ApartmentImage.objects.create(apartment=apartment, image=img)
#             return redirect('apartments')  # Redirect after successful submission
#     else:
#         form = ApartmentForm()
#
#     # Render the form for GET requests or invalid submissions
# #    return render(request, 'addApartment.html', {'form': form})
from django.db import transaction

from django.db import transaction

@login_required
def add_apartment(request):
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        image_form = ImagesForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            # התחל טרנזקציה
            with transaction.atomic():
                # יצירת דירה
                apartment = Apartment.objects.create(
                    owner=request.user,
                    city=form.cleaned_data['city'],
                    neighborhood=form.cleaned_data['neighborhood'],
                    street=form.cleaned_data['street'],
                    price=form.cleaned_data['price'],
                    rooms=form.cleaned_data['rooms'],
                    floor=form.cleaned_data['floor'],
                    description=form.cleaned_data['description'],
                    isBrokerage=form.cleaned_data['isBrokerage'],
                )

                # עכשיו התמונות יתווספו אחרי שהדירה נשמרה
                images = request.FILES.getlist('image')
                for img in images:
                    ApartmentImage.objects.create(apartment=apartment, image=img)

            return redirect('apartments')  # הפניה לאחר הצלחה

    else:
        form = ApartmentForm()
        image_form = ImagesForm()

    return render(request, 'addApartment.html', {'form': form, 'image_form': image_form})

@login_required
def sell_apartment(request, apartmentId):
    apartment = get_object_or_404(Apartment, id=apartmentId)
    if not request.user.seller:
        return HttpResponseForbidden("אין לך הרשאה להוסיף דירה")
    if request.method == 'POST':
        apartment.isSold = True
        apartment.save()
        if apartment.isBrokerage:
            apartment.commission = (apartment.price / 100) * 2
            apartment.save()
    return render(request, 'sellerApartments.html', {'apartment': apartment, 'request': request})
