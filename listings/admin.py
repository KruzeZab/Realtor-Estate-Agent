from django.contrib import admin
from .models import Listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'realtor', 'price', 'is_published']
    list_display_links = ['id', 'title']
    list_editable = ['is_published', ]
    list_filter = ['price', 'is_published']
    search_fields = ['title', 'realtor']
    list_per_page = 25
    list_filter = ['state', ]

admin.site.register(Listing, ListingAdmin)
