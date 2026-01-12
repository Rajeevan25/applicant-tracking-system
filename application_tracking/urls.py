from django.urls import path
from . import views

app_name = 'application_tracking'

urlpatterns = [
    path('create/', views.create_advertisement, name='create_advertisement'),
    path("<uuid:advertisement_id>/", views.get_advertisement, name='get_advertisement'),
]