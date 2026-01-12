from django.shortcuts import render
from .forms import  JobAdvertisementForm
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import JobAdvertisement
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages


@login_required
def create_advertisement(request:HttpRequest):
    """Create a new application"""
    form = JobAdvertisementForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance: JobAdvertisement = form.save(commit=False)
        instance.posted_by = request.user
        instance.save()

        messages.success(request,"Advertisement created, You can now receive applications." )
        return redirect(instance.get_absolute_url())
    
    context = {
        "job_advert_form":form,
        "title":"Create a new advertisement",
        "btn_text":"Create advertisement"
    }

    return render(request, 'create_advert.html',context)



def get_advertisement(request:HttpRequest, advertisement_id):
    job_advertisement = get_object_or_404(JobAdvertisement,pk = advertisement_id)
    
    context = {
        "job_advertisement":job_advertisement
    }
    return render(request, 'advert.html', context)

def advertisement_list(request):
    return render(request, 'application_tracking/advertisement_list.html') 

def update_advertisement(request, advertisement_id):
    return render(request, 'application_tracking/update_advertisement.html', {'advertisement_id': advertisement_id})

def delete_advertisement(request, advertisement_id):
    return render(request, 'application_tracking/delete_advertisement.html', {'advertisement_id': advertisement_id})    

def apply_to_advertisement(request, advertisement_id):
    return render(request, 'application_tracking/apply_to_advertisement.html', {'advertisement_id': advertisement_id})

def my_applications(request):
    return render(request, 'application_tracking/my_applications.html')

def my_job_advertisements(request):
    return render(request, 'application_tracking/my_job_advertisements.html')



