from django.urls import path
from . import views

app_name = 'application_tracking'

urlpatterns = [
    path('create/', views.create_advertisement, name='create_advertisement'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-job-advertisements/', views.my_job_advertisements, name='my_job_advertisements'),
    path("<uuid:advertisement_id>/", views.get_advertisement, name='get_advertisement'),
    path('<uuid:advertisement_id>/apply/', views.apply_to_advertisement, name='apply_to_advertisement'),

]