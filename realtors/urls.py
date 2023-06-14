from django.urls import path

from . import views

app_name = 'realtors'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.RealtorView.as_view(), name='realtor'),
    path('search/', views.SearchView.as_view(), name='search'),
]
