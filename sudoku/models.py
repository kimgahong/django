from django.db import models

class Post(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    text = models.TextField()

Post.objects.all() # 모든 변수를 가져오는 것 

class Ranking(models.Model):
    name = models.CharField(max_length=255)
    elapsed_time = models.TimeField()

# Create your models here.
