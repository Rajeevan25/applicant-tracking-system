from django.utils import timezone
from django.shortcuts import render

from core.models import CustomUser
from .forms import  JobAdvertisementForm, JobApplicationForm, JobApplication
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from .models import JobAdvertisement
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator

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
    form = JobApplicationForm()
    job_advertisement = get_object_or_404(JobAdvertisement,pk = advertisement_id)
    
    context = {
        "job_advertisement":job_advertisement,
        "application_form":form,
    }
    return render(request, 'advert.html', context)

def advertisement_list(request:HttpRequest):
    active_advertisements = JobAdvertisement.objects.filter(is_published=True,deadline__gte=timezone.now().date())
    paginator = Paginator(active_advertisements, 10)  # Show 10 advertisements per page
    page_number = request.GET.get('page')
    active_advertisements = paginator.get_page(page_number)
    context = {
        "job_adverts":active_advertisements}
    print(context)
    return render(request, 'home.html', context)

def update_advertisement(request, advertisement_id):
    return render(request, 'application_tracking/update_advertisement.html', {'advertisement_id': advertisement_id})

def delete_advertisement(request, advertisement_id):
    return render(request, 'application_tracking/delete_advertisement.html', {'advertisement_id': advertisement_id})    

def apply_to_advertisement(request:HttpRequest, advertisement_id):
    job_advertisement = get_object_or_404(JobAdvertisement,pk = advertisement_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            if job_advertisement.applications.filter(email=email).exists():
                messages.error(request, "You have already applied to this job advertisement with this email.")
                return redirect('application_tracking:get_advertisement', advertisement_id=advertisement_id) 
            
            application : JobApplication = form.save(commit=False)
            application.job_advertisement = job_advertisement
            application.save()
            messages.success(request, "Your application has been submitted successfully.")
            return redirect('application_tracking:get_advertisement', advertisement_id=advertisement_id)
    else:
        form = JobApplicationForm()
    context = {
        'application_form': form,
        'job_advertisement': job_advertisement,
    }
    return render(request, 'advert.html', context)


@login_required
def my_applications(request:HttpRequest):
    user : CustomUser = request.user
    applications = JobApplication.objects.filter(email=user.email)
    paginator = Paginator(applications,10)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    context ={
        "my_applications": applications  
          }
    print(context)
    return render(request, 'my_applications.html',context)

@login_required
def my_job_advertisements(request:HttpRequest):
    user: CustomUser = request.user
    advertisements = JobAdvertisement.objects.filter(posted_by=user)
    paginator = Paginator(advertisements, 10)
    page_number = request.GET.get('page')
    advertisements = paginator.get_page(page_number)
    context = {
        "my_jobs": advertisements,
        "current_date": timezone.now().date()
        }
    return render(request, 'my_jobs.html', context)
