from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from realtors.models import Realtor

# Create your views here.
class IndexView(ListView):
    template_name = 'realtors/realtors.html'
    context_object_name = 'realtors'
    paginate_by = 6

    def get_queryset(self):
        return Realtor.objects.order_by('-hire_date').all()

class RealtorView(DetailView):
    model = Realtor
    template_name = 'realtors/realtor.html'
    context_object_name = 'realtor'

class SearchView(ListView):
    template_name = 'realtors/search.html'
    context_object_name = 'realtors'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        result = Realtor.objects.order_by('-hire_date').all()
        return result.filter(name__icontains=query)
        


    
