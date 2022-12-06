from django.db import models
from django.contrib.auth.models import User

class ApplianceType(models.Model):
    '''Model Representing appliance type'''
    type = models.CharField(max_length=50, help_text='Type of the appliance')

    class Meta:
        verbose_name = 'Type of Appliance'
        verbose_name_plural = 'Types of Appliances'

    def __str__(self):
        return f'{self.type}'

class Appliance(models.Model):
    """Model representing a specific appliance"""
    title = models.CharField(max_length=50, help_text='Name\Title of the device')
    location = models.CharField(max_length=50, default=None, help_text='Location of the device')
    type = models.ForeignKey('ApplianceType', on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=50, help_text='Unique ID number, for engineering department')
    description = models.CharField(max_length=1024, blank=True, null=True, default=None, help_text='Desciption of the device')
    image_url = models.CharField(max_length=512, blank=True, null=True, default=None, help_text='Image URL for the device')

    APPLIANCE_STATUS = (
        ('a', 'Functional'),
        ('b', 'Under repair')
    )

    status = models.CharField(
        max_length=1,
        choices=APPLIANCE_STATUS,
        blank=True,
        default='a',
        help_text='Status of the appliance'
    )

    def __str__(self):
        return f'{self.title}, {self.location}, {self.type}'

    class Meta:
        verbose_name = 'Appliance'
        verbose_name_plural = 'Appliances'

class Booking(models.Model):
    """Model representing a booking - appliance, time and user"""
    appliance = models.ForeignKey('Appliance', on_delete=models.SET_NULL, null=True)
    day_from = models.DateTimeField(null=True)
    day_to = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.appliance.title}, {self.day_from} {self.day_to}'

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'