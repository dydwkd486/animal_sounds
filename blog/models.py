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
    LEVEL = (
        ('m','Mammalia'),#포유류
        ('b','Birds'), #조류
        ('r','Reptile'), #파충류
        ('a','Amphibia'), # 양서류
        ('i','Insect'), # 곤충
        )
    ADDRESS = (
        ('a','서울특별시'),#
        ('b','경기도'),#
        ('c','강원도'),#
        ('d','충청북도'),#
        ('e','충청남도'),#
        ('f','경상북도'),#
        ('g','경상남도'),#
        ('h','전라북도'),#
        ('i','전라남도'),
        ('j','제주도'),
        ('k','북한'))
    LEVEL_DICT = {'m':'Mammalia', 'b':'Birds', 'r':'Reptile', 'a':'Amphibia', 'i':'Insect'}
    ADDRESS_DICT = {'a': '서울특별시','b': '경기도','c': '강원도','d': '충청북도','e': '충청남도','f': '경상북도','g': '경상남도',
        'h': '전라북도','i': '전라남도','j': '제주도','k': '북한', '1':'test'}

    writer = models.CharField(max_length = 100)
    animalclass = models.CharField(max_length=1,choices=LEVEL, blank=True, default='m', help_text='class_Level')
    title = models.CharField(max_length = 20, blank=True, null=True)
    Latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    Longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    address = models.CharField(max_length=1,choices=ADDRESS, blank=True, default='a', help_text='address_Level')
    content = models.TextField(blank=True, null=True)
    imagefile = models.FileField(null=False, upload_to='img')
    soundfile = models.FileField(null=False, upload_to='sound')
    file_size_input =models.IntegerField(null=True)
    file_name_input = models.CharField(max_length = 30,null=True)
    file_ex_input = models.CharField(max_length = 10,null=True)
    duration_input = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    observed_date=models.DateField(default=timezone.now, null=True)
    created_date = models.DateTimeField(default=timezone.now)

class Animal_Sub_file(models.Model):
    Animal_map = models.ForeignKey(Animal_map, on_delete=models.CASCADE)
    file= models.FileField(null=True, upload_to='subsound')
    label= models.CharField(null=True,max_length = 30)
    start_point= models.DecimalField(max_digits=10, decimal_places=7, null=True)
    end_point= models.DecimalField(max_digits=10, decimal_places=7, null=True)
    file_size_input =models.IntegerField(null=True)
    file_name_input =models.CharField(max_length = 30,null=True)
    file_ex_input = models.CharField(max_length = 10,null=True)
    duration_input = models.IntegerField(null=True)
''' end 승원 수정 부분 '''

class Animal_total_info(models.Model):
    name = models.CharField(max_length = 20)
    content = models.TextField()

class district(models.Model):
    CTPRVN_CD=models.IntegerField(null=False)
    CTP_ENG_NM = models.TextField(null=True)
    CTP_KOR_NM = models.TextField(null=True)
    WKT = models.TextField(null=True)



