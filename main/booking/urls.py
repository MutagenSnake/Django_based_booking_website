from django.urls import path
from . import views

urlpatterns =[
    path('home/', views.homepage, name='home'),
    path('equipment/', views.equipment, name='equipment'),
    path('register/', views.register, name='register'),
    path('booking/<int:appliance_id>', views.booking, name='booking'),
]