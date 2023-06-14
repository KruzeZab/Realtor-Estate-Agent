from django.shortcuts import render
from django.views.generic import ListView

from listings.models import Listing
from realtors.models import Realtor

# Create your views here.
class IndexView(ListView):
    template_name = 'pages/index.html'
    context_object_name = 'listings'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['realtors'] = Realtor.objects.order_by('-hire_date')[:3]
        return context

    def get_queryset(self):
        return Listing.objects.order_by('-list_date').filter(is_published=True)[:3]



def about(request):
    return render(request, 'pages/about.html', {})

def contact(request):
    return render(request, 'pages/contact-us.html', {})
