from django.contrib import admin
from .models import Appliance, Booking, ApplianceType

class ApplianceInline(admin.TabularInline):
    model = Appliance
    fields = ('title', 'location', 'status',)
    readonly_fields = ('title', 'location',)
    can_delete = False
    extra = 0

class ApplianceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'type',  'status')
    list_filter = ('type', 'status')
    search_fields = ('id', 'title', 'location', 'type__type')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('appliance', 'user', 'day_from', 'day_to')

class ApplianceTypeAdmin(admin.ModelAdmin):
    inlines = [ApplianceInline]

admin.site.register(Appliance, ApplianceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(ApplianceType, ApplianceTypeAdmin)
