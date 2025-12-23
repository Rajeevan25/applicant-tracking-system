from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # User login
    path('logout/', views.logout, name='logout'),  # User logout
    path('register/', views.register, name='register'), # User registration
    path('verify-account/', views.verify_account, name='verify_account'), # Account verification
    path('', views.home, name='home'),  # Home page
    path('forgot-password/', views.reset_password, name='reset_password'), # Password reset
    path("reset-password-confirm/", views.reset_password_confirm, name="reset_password_confirm"),  # Password reset confirmation
    path('set-new-password/', views.set_new_password, name='set_new_password'), # Set new password
]