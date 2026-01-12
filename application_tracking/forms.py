from django.forms import Form, CharField, ChoiceField, IntegerField, DateField, URLField, Textarea, ModelForm
from .models import JobAdvertisement, JobApplication
from .enums import EmploymentStatus, ExperienceLevel, LocationTypeChoice, EducationLevel, LocationType
from django import forms

class JobAdvertisementForm(ModelForm):
    class Meta:
        model = JobAdvertisement
        fields = [
            'title', 'description', 'job_type', 'company_name', 'employment_type',
            'experience_level', 'location', 'is_published', 'deadline', 'skills'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Job Title','class': 'form-control'}),
            'description': Textarea(attrs={'rows': 4, 'placeholder': 'Job Description','class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Company Name','class': 'form-control'}),
            'location': forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Location','class': 'form-control'}),
            'employment_type': forms.Select(choices=EmploymentStatus, attrs={'class': 'form-control'}),
            'experience_level': forms.Select(choices=ExperienceLevel, attrs={'class': 'form-control'}),
            'job_type': forms.Select(choices=LocationTypeChoice, attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={ 'placeholder': 'comma separated skills','class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date','placeholder': 'YYYY-MM-DD','class': 'form-control'}),
        }

class JobApplicationForm(ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'name', 'email', 'portfolio_url', 'resume', 'cover_letter'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'maxlength': 255, 'placeholder': 'Your Name','class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email','class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'Portfolio URL','class': 'form-control'}),
            'resume': forms.ClearableFileInput(attrs={'placeholder': 'Upload Resume','class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'cover_letter': Textarea(attrs={'rows': 4, 'placeholder': 'Cover Letter','class': 'form-control'}),
        }   
