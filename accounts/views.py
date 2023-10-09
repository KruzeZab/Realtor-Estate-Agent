from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages, auth
from .models import Contact
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated:
        return redirect('pages:index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return HttpResponseRedirect('/accounts/'+str(request.user.id))
        else:
            messages.error(request, 'Invalid credentials')
            return HttpResponseRedirect('/accounts/login')
    else:
        return render(request, 'accounts/login.html')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
        # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return HttpResponseRedirect('/accounts/register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return HttpResponseRedirect('/accounts/register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    # Login after register
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in')
                    return HttpResponseRedirect('/listings')
                    
        else:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect('/accounts/register')
    else:
        return render(request, 'accounts/register.html')

class ProfileView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'accounts/profile.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return Contact.objects.filter(user_id=self.request.user.id)
    

def logoutView(request):
    messages.success(request, 'You are now logged out!')
    logout(request)
    return HttpResponseRedirect('/accounts/login')
