from django.db import models
from common.models import BaseModel
from core.models import CustomUser
from .enums import  ExperienceLevel, LocationTypeChoice, EducationLevel, LocationType, EmploymentStatus , ApplicationStatus
from django.urls import reverse

class JobAdvertisement(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=100, choices=LocationTypeChoice)
    company_name = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=100, choices=EmploymentStatus)
    experience_level = models.CharField(max_length=100, choices=ExperienceLevel)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=True)
    deadline = models.DateField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True, max_length=1000)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_advertisements')

    class Meta:
        db_table = 'job_advertisements'
        ordering = ['-created_at',]

    def publish(self):
        self.is_published = True
        self.save(update_fields=['is_published'])
    
    @property
    def total_applications(self) -> int:
        return self.applications.count()
    
    def get_absolute_url(self):     
        return reverse('application_tracking:get_advertisement', kwargs={'advertisement_id': self.id})

class JobApplication(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    portfolio_url = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True, max_length=2000)
    status = models.CharField(max_length=100, choices=ApplicationStatus.choices, default=ApplicationStatus.APPLIED)
    job_advertisement = models.ForeignKey(JobAdvertisement, on_delete=models.CASCADE, related_name='applications')