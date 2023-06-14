from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
