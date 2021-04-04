from django.db import models
from django.utils import timezone

# import os
#
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
#
# import time
# import librosa
# import numpy as np
# import tensorflow as tf
# from datetime import datetime
# from modules.models import Model, Solver, nClass, Feature_class, cos_sim



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
        ('k','북한'),
        ('l','세종시'),
        ('m','인천'),
        ('n','대전'),
        ('o','울산'),
        ('p','대구'),
        ('q','부산'))
    LEVEL_DICT = {'m':'Mammalia', 'b':'Birds', 'r':'Reptile', 'a':'Amphibia', 'i':'Insect'}
    ADDRESS_DICT = {'a': '서울특별시','b': '경기도','c': '강원도','d': '충청북도','e': '충청남도','f': '경상북도','g': '경상남도',
        'h': '전라북도','i': '전라남도','j': '제주도','k': '북한', 'l': '세종시', 'm': '인천', 'n': '대전', 'o': '울산', 'p': '대구', 'q': '부산', '1':'test'}

    writer = models.CharField(max_length = 100)
    animalclass = models.CharField(max_length=1,choices=LEVEL, blank=True, default='m', help_text='class_Level')
    title = models.CharField(max_length = 100, blank=True, null=True)
    title1 = models.CharField(max_length=100, blank=True, null=False)
    Latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    Longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    address1 = models.CharField(max_length = 30,null=True)
    address2 = models.CharField(max_length=30, null=True)
    address3 = models.CharField(max_length=30, null=True)
    address4 = models.CharField(max_length=30, null=True)
    address5 = models.CharField(max_length=30, null=True)
    address6 = models.CharField(max_length=30, null=True)
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
'''내부 디비 부분'''
class Animal_total_info(models.Model):
    name = models.CharField(max_length = 50)
    scientific_name= models.CharField(max_length = 50)
    redlist = models.CharField(max_length = 20)
    food = models.TextField()
    habitat = models.TextField()
    content = models.TextField()
'''내부 디비 부분 end'''
class district(models.Model):
    CTPRVN_CD=models.IntegerField(null=False)
    CTP_ENG_NM = models.TextField(null=True)
    CTP_KOR_NM = models.TextField(null=True)
    WKT = models.TextField(null=True)

class UploadFileModel(models.Model):
    soundfile = models.FileField(null=False,upload_to='temporary')

# def time_string():
#     return datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
#
# class Classification(models.Model):
#     def predict(self):
#         # if request.method == 'POST':
#         fs = 44100
#         print(os.listdir('./media/temporary')[0])
#         inp_wav = os.path.join('./test1.wav')
#         # inp_wav = os.path.join(os.listdir('./media/temporary')[0])
#         # inp_wav = os.path.join(value1)
#         print(inp_wav)
#         out_txt = os.path.join('./animal.log')
#         # print(out_txt)
#         prev_state = None
#         with open("./class_name.txt", "r", encoding='UTF8') as f:
#             labels = f.readlines()
#         labels = np.block(labels)
#         labels = list(map(lambda s: s.strip(), labels))
#
#         with tf.Session() as sess:
#             model_A = Model('A')
#             model_A_solver = Solver(sess, model_A)
#
#             # while True:
#             curr_state = os.path.getatime(inp_wav)
#             if curr_state != prev_state:
#                 print(time_string(), end=' ')
#                 print("New recorded file arrived!")
#                 prev_state = curr_state
#
#                 wav, _ = librosa.load(inp_wav, sr=fs)
#                 duration = len(wav) // fs
#                 wav = wav[np.newaxis, :]
#
#                 hop_size = fs // 2
#                 total_steps = duration * 2 - 1
#
#                 for i in range(total_steps):
#                     inp = wav[:, i * hop_size:(i + 1) * hop_size + hop_size]
#                     Sc = model_A_solver.evaluate(inp)
#                     Sc = np.asarray(Sc, dtype=np.float32)[0]
#
#                     rres = list()
#                     for ii in range(nClass):
#                         rres.append(cos_sim(Sc, Feature_class[ii]))
#                     rres = np.transpose(np.block(np.transpose(rres)))
#                     classs = np.where(rres > 0.92)[0]
#
#                     if not classs:
#                         print('No animal sound detected')
#                     else:
#                         curr_time = time.gmtime(curr_state + (i * .5))
#                         with open(out_txt, 'a', encoding='UTF8') as f:
#                             f.write(str(labels[classs.item()]) + ' sound detected at '
#                                     + time.strftime('%Y/%m/%d-%H:%M:%S', curr_time) + '\n')
#                         # print(time_string(), end=' ')
#                         # print(str(labels[classs.item()]) + ' sound detected')
#                         print(labels[classs.item()])
#                         labelsdata = labels[classs.item()]
#         sess.close()
#         return labelsdata
