from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages

from listings.models import Listing
from accounts.models import Contact


class IndexView(ListView):
    template_name = 'listings/listings.html'
    context_object_name = 'listings'
    paginate_by = 6

    def get_queryset(self):
        return Listing.objects.order_by('-list_date').all()


class ListingView(DetailView):
    template_name = 'listings/listing.html'
    context_object_name = 'listing'
    model = Listing   

class SearchView(ListView):
    template_name = 'listings/search.html'
    context_object_name = 'listings'
    model = Listing
    paginate_by = 6

    def get_queryset(self):
        result = Listing.objects.order_by('-list_date').filter(is_published=True)

        keywords = self.request.GET.get('keywords', None)
        if keywords:
            result = result.filter(title__icontains=keywords)

        city = self.request.GET.get('city', None)
        if city:
            result = result.filter(city__icontains=city)

        state = self.request.GET.get('state', None)
        if state:
            result = result.filter(state__iexact=state)
        
        return result

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        address = request.POST['address']
        message = request.POST['message']
        user_id = request.POST['user_id']

        username = request.user

        contacted = Contact.objects.all().filter(property_id=listing_id, user_id=user_id)
        if contacted:
            messages.error(request, 'You have already enquired about the property.')
            return redirect('/listings/'+listing_id)
        else:
            Contact.objects.create(user_id=user_id, property_id=listing_id, property_name=listing, message=message)
            messages.success(request, 'Added to enquiry. Check your dashboard.')
            return redirect('/listings/'+listing_id)
    else:
        return redirect('/listings/'+listing_id)




    


