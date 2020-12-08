from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.logoutView, name='logout')
]
