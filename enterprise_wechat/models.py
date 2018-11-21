from django.db import models
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class EnterpriseWechatApp(models.Model):
    corp_id = models.CharField(max_length=1024)
    corp_secret = models.CharField(max_length=1024)
    agent_id = models.CharField(max_length=1024)
    remark = models.TextField(default='')
    message_callback_url = models.CharField(max_length=1024, default="")
    message_token = models.CharField(max_length=1024, default="")
    message_aes_key = models.CharField(max_length=1024, default="")

    def __str__(self):
        return "%s_%s" % (self.corp_id, self.remark)


class EnterpriseWechatAccessToken(models.Model):
    access_token = models.CharField(max_length=1024)
    expire_in = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    # Every access_token is belong to a app.
    enterprise_wechat_app = models.ForeignKey(
        EnterpriseWechatApp, on_delete=models.CASCADE)

    def is_expire(self):
        return timezone.now() > (self.created + timedelta(seconds=self.expire_in))

    def __str__(self):
        return "token_%s_%s" % (self.enterprise_wechat_app, self.access_token)


class EnterpriseWechatUser(models.Model):
    user_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=32)
    gender = models.IntegerField(default=0)
    avatar = models.CharField(max_length=1024)

    def __str__(self):
        return self.name