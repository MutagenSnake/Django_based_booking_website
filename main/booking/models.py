from django.db import models
from django.contrib.auth.models import User

class Appliance(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50, default=None)
    number = models.CharField(max_length=50)
    description = models.CharField(max_length=1024, blank=True, null=True, default=None)
    image_url = models.CharField(max_length=512, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.title}, {self.location}'

class Booking(models.Model):
    appliance = models.ForeignKey('Appliance', on_delete=models.SET_NULL, null=True)
    day_from = models.DateTimeField(null=True)
    day_to = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.appliance.title}, {self.day_from} {self.day_to}'