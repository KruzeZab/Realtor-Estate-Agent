import joblib
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma


from queue import PriorityQueue

from listings.models import Listing
from accounts.models import Contact

from django.conf import settings
from django.core.mail import send_mail

def get_recommendation(current_item):
    # Content Filtering

    # Initialize a priority Queue
    recom = PriorityQueue()

    # Weight and prev Weight
    weight = 0
    prev_weight = 0

    # Get all listings except current one
    listings = Listing.objects.filter(is_published=True).exclude(id=current_item.id)

    # loop through and assign weights according to weightage
    for listing in listings:
        # Price = 4, State = 3 and City = 2 are given highy priority
        # While others = 1
        if current_item.address == listing.address:
            weight += 1

        if current_item.city == listing.city:
            weight += 2

        if current_item.state == listing.state:
            weight += 3

        if current_item.price == listing.price:
            weight += 4

        if current_item.bedrooms == listing.bedrooms:
            weight += 1


        if current_item.bathrooms == listing.bathrooms:
            weight += 1

        if current_item.garage == listing.garage:
            weight += 1

        if current_item.sqft == listing.sqft:
            weight += 1

        if current_item.lot_size == listing.lot_size:
            weight += 1

        # push to queue
        if weight > prev_weight:
            recom.put((weight, listing))
            prev_weight = weight
            weight = 0

    # Cast to list to return the top 3 recommendations
    result = []

    while not recom.empty():
        result.append(recom.get()[1])

        # break when 3 entries 
        if len(result) == 3:
            break
        
    return result


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recoms'] = get_recommendation(self.object)
        return context

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
            # send email
            subject = 'Enquirt about Property'
            message = f'Dear Realtor, \n\n {username} has enquired about the property {listing} located at {address}. \n\n Message: {message} \n\n Thank you.'
            email_from = settings.EMAIL_HOST_USER
            print(Listing.objects.get(id=listing_id).realtor.email)
            recipient_list = [Listing.objects.get(id=listing_id).realtor.email, ]
            send_mail( subject, message, email_from, recipient_list )

            return redirect('/listings/'+listing_id)
    else:
        return redirect('/listings/'+listing_id)



def get_predicted_price(new_data):
    # newData = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot']
    model = joblib.load('./algorithm/linear_regression_model.pkl')
    predicted_price = model.predict([new_data])
    return predicted_price[0]

def predict(request):
    if request.method == 'POST':
        bedrooms = int(request.POST['bedrooms'])
        bathrooms = int(request.POST['bathrooms'])
        sqft_living = int(request.POST['sqft-living'])
        sqft_lot = int(request.POST['sqft-lot'])
        floor = int(request.POST['floor'])
        waterfront = int(request.POST['waterfront'])
        view = int(request.POST['view'])
        condition = int(request.POST['condition'])

        new_data = [bedrooms, bathrooms, sqft_living, sqft_lot, floor, waterfront, view, condition]

        predicted_price = get_predicted_price(new_data)

        formatted_price = f'{intcomma(int(predicted_price))}'

        messages.success(request, f'Predicted Price: $ {formatted_price}')

        return redirect('/listings/predict')
    return render(request, 'listings/predict.html')
    


