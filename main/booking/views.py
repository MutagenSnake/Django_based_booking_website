from rest_framework import generics
from .serializers import BookingSerializer
from .models import Appliance, Booking
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, User
from django.shortcuts import render
from .forms import BookingForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
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

@csrf_protect
def register(request):
    if request.method == 'GET':
        return render(request, template_name='registration/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, f'{username} is taken')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, f'{email} is taken')
                        return redirect('register')
                    else:
                        User.objects.create_user(username=username, email=email, password=password)
                        messages.info(request, f'{username} registration successful!')
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        return redirect('home')
        else:
            messages.error(request, f'Invalid Form {form.errors.as_data()}')
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

                elif (datetime_from > datetime_to):
                    messages.error(request, 'Mixed up past and future!')
                    return render(request, template_name='bookingpage.html', context=context)

                else:
                    continue

            if past_checker(datetime_from) == True:
                messages.error(request, 'The booking time already have passed')
                return render(request, template_name='bookingpage.html', context=context)

            else:
                messages.success(request, 'Booked successfully')
                Booking.objects.create(appliance=appliance, day_from=datetime_from, day_to=datetime_to, user=request.user)
                return render(request, template_name='bookingpage.html', context=context)

        else:
            messages.success(request, 'Booked successfully, first booking!')
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

def profile(request):
    return render(request, template_name='profile.html')