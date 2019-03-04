from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length = 20)
    content = models.TextField()

class Animal(models.Model):
    name = models.CharField(max_length = 20)
    content = models.TextField()

class Animal_map(models.Model):
    writer = models.CharField(max_length = 100)
    title = models.CharField(max_length = 20)
    Latitude = models.DecimalField(max_digits=10, decimal_places=7)
    Longitude = models.DecimalField(max_digits=10, decimal_places=7)
    content = models.TextField()
    file = models.FileField(null=False, upload_to='img')
    soundfile = models.FileField(null=False, upload_to='sound')
    observed_date=models.DateTimeField(blank=True, null=False)
    created_date = models.DateTimeField(default=timezone.now)