from django.db import models
from datetime import datetime, timedelta
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

    def __unicode__(self):
        return "%s:%s" % (self.corp_id, self.remark)


class EnterpriseWechatAccessToken(models.Model):
    access_token = models.CharField(max_length=1024)
    expire_in = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    # Every access_token is belong to a app.
    enterprise_wechat_app = models.ForeignKey(EnterpriseWechatApp, on_delete=models.CASCADE)

    def is_expire(self):
        return timezone.now() > (self.created + timedelta(seconds=self.expire_in))

