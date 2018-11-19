from django.db import models


# Create your models here.
class User(models.Model):
    user_type = models.CharField(max_length=32)
    wework_id = models.CharField(max_length=128, default="")
    avatar_url = models.CharField(max_length=1024, default="")
    sex = models.CharField(max_length=4, default="未设置")
