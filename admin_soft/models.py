from django.db import models
from django.utils import timezone

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Purpose(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    CUSTOM_FIELD = [
        ('Business', 'Business Meeting'),
        ('Support', 'Customer Support'),
        ('Consultation', 'Consultation'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)  # Required
    email = models.EmailField(blank=True, null=True)  # Optional 
    phone_number = models.IntegerField()  # Required and unique
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  # ForeignKey to Department model
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)  # ForeignKey to Purpose model
    other_purpose = models.CharField(max_length=255, blank=True, null=True)  # Optional additional detail
    organization = models.CharField(max_length=255, blank=True, null=True)
    review = models.TextField(blank=True)  
    time = models.DateTimeField(default=timezone.now)  # Add default value
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Review by {self.name or 'Anonymous'}"
    



