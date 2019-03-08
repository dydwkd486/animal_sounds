from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length = 20)
    content = models.TextField()

class Animal(models.Model):
    name = models.CharField(max_length = 20)
    content = models.TextField()

''' 승원 수정 부분 '''

class Animal_map(models.Model):
    writer = models.CharField(max_length = 100)
    title = models.CharField(max_length = 20)
    Latitude = models.DecimalField(max_digits=10, decimal_places=7)
    Longitude = models.DecimalField(max_digits=10, decimal_places=7)
    content = models.TextField()
    imagefile = models.FileField(null=False, upload_to='img')
    soundfile = models.FileField(null=False, upload_to='sound')
    file_size_input =models.IntegerField(null=True)
    file_name_input =models.CharField(max_length = 30,null=True)
    file_ex_input = models.CharField(max_length = 10,null=True)
    duration_input = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    observed_date=models.CharField(max_length = 20)
    created_date = models.DateTimeField(default=timezone.now)



class Animal_Sub_file(models.Model):
    Animal_map = models.ForeignKey(Animal_map, on_delete=models.CASCADE)
    file= models.FileField(null=True, upload_to='subsound')
    label= models.CharField(null=True,max_length = 30)
    start_point= models.DecimalField(max_digits=10, decimal_places=7, null=True)
    end_point= models.DecimalField(max_digits=10, decimal_places=7, null=True)
    #file_size_input =models.IntegerField(null=True)
    #file_name_input =models.CharField(max_length = 30,null=True)
    #file_ex_input = models.CharField(max_length = 10,null=True)
    #duration_input = models.IntegerField(null=True)
''' end 승원 수정 부분 '''


