import datetime
from django.shortcuts import render
from rest_framework import generics
from .serializers import BookingSerializer
from django.shortcuts import render, redirect
from .models import Appliance, Booking, ApplianceType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .forms import BookingForm
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import re
from .functions import form_to_datetime, overlap_checker, past_checker, json_serial
from django.core.paginator import Paginator
from django.db.models import Q
import json

def homepage(request):
    """Homepage view"""
    return render(request, template_name='index.html')

def equipment(request):
    """ View listing all equipment with search option and redirection to booking"""
    paginator = Paginator(Appliance.objects.all(), 10)
    page_number = request.GET.get('page')
    paged_appliances = paginator.get_page(page_number)
    context = {
        'items': paged_appliances,
    }
    return render(request, template_name='equipment.html', context=context)

def register(request):
    if request.method == 'GET':
        return render(request, template_name='registration/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')

@csrf_protect
def booking(request, appliance_id):
    form = BookingForm
    appliance = Appliance.objects.get(pk=appliance_id)
    context = {'appliance': appliance, 'form': form}
    if request.method == "POST":
        time_from = request.POST['timeFrom']
        time_to = request.POST['timeTo']

        datetime_from = form_to_datetime(time_from)
        datetime_to = form_to_datetime(time_to)

        #booking overlap check
        all_bookings = appliance.booking_set.all()
        if all_bookings:
            for booking in all_bookings:
                start = booking.day_from
                end = booking.day_to

                if overlap_checker(start, end, datetime_from, datetime_to) == True:
                    messages.error(request, 'The booking time overlaps with other booking')
                    return render(request, template_name='bookingpage.html', context=context)

                elif past_checker(datetime_from) == True:
                    messages.error(request, 'The booking time already have passed')
                    return render(request, template_name='bookingpage.html', context=context)

                else:
                    messages.success(request, 'Booked successfully')
                    Booking.objects.create(appliance=appliance, day_from=datetime_from, day_to=datetime_to, user=request.user)
                    return render(request, template_name='bookingpage.html', context=context)

        else:
            messages.success(request, 'Booked successfully')
            Booking.objects.create(appliance=appliance, day_from=datetime_from, day_to=datetime_to, user=request.user)
            return render(request, template_name='bookingpage.html', context=context)

    if request.method == 'GET':
        all_bookings = appliance.booking_set.all()
        booking_data = []
        if all_bookings:
            for booking in all_bookings:
                start = booking.day_from
                end = booking.day_to
                booking_data += [[start, end]]

        data = json.dumps(booking_data, default=json_serial)
        context = {'appliance': appliance, 'form': form, 'data': data}
        return render(request, template_name='bookingpage.html', context=context)

def search(request):
    query = request.GET.get('query')
    search_results = Appliance.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    context = {
        'items': search_results,
    }
    return render(request, template_name='equipment.html', context=context)

class Bookinglist(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer