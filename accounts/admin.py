from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_id',  'property_name', 'property_id']
    list_display_links = ['property_id', 'user_id', 'property_name']
    list_per_page = 50

# Register your models here.
admin.site.register(Contact, ContactAdmin)
