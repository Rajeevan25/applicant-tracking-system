from django.db import models
from common.models import BaseModel

EmploymentStatus = [
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Contract', 'Contract'),
    ('Internship', 'Internship'),
    ('Temporary', 'Temporary'),
    ('Volunteer', 'Volunteer'),
    ('Other', 'Other'), 
]

ExperienceLevel = [
    ('Entry Level', 'Entry Level'),
    ('Mid Level', 'Mid Level'),
    ('Senior Level', 'Senior Level'),
    ('Director', 'Director'),
    ('Executive', 'Executive'), 
    ('Internship', 'Internship'),
    ('Not Applicable', 'Not Applicable'),
]

LocationTypeChoice = [
    ('On-site', 'On-site'),
    ('Remote', 'Remote'),
    ('Hybrid', 'Hybrid'),
    ('Not Applicable', 'Not Applicable'),
]
EducationLevel = [
    ('High School', 'High School'),
    ('Associate Degree', 'Associate Degree'),
    ('Bachelor\'s Degree', 'Bachelor\'s Degree'),
    ('Master\'s Degree', 'Master\'s Degree'),
    ('Doctorate', 'Doctorate'),
    ('Professional Certification', 'Professional Certification'),
    ('Not Applicable', 'Not Applicable'),
]

LocationType = [
    ('Urban', 'Urban'),
    ('Suburban', 'Suburban'),
    ('Rural', 'Rural'),
    ('Not Applicable', 'Not Applicable'),
]

class ApplicationStatus(models.TextChoices):
    APPLIED = 'Applied', 'Applied'
    UNDER_REVIEW = 'Under Review', 'Under Review'
    INTERVIEW_SCHEDULED = 'Interview Scheduled', 'Interview Scheduled'
    OFFER_EXTENDED = 'Offer Extended', 'Offer Extended'
    REJECTED = 'Rejected', 'Rejected'