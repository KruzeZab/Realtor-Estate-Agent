from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.ListingView.as_view(), name='listing'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('contact/', views.contact, name='contact'),
    path("predict/", views.predict, name="predict")
]
