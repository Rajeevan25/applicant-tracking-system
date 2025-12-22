from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # User login
    path('logout/', views.logout, name='logout'),  # User logout
    path('register/', views.register, name='register'), # User registration
    path('verify-account/', views.verify_account, name='verify_account'), # Account verification
    path('', views.home, name='home'),  # Home page
]