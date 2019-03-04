from django.contrib import admin
from .models import Post,Animal,Animal_map
# Register your models here.
admin.site.register(Post)
admin.site.register(Animal)
admin.site.register(Animal_map)