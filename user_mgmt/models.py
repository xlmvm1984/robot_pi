from django.db import models
from enterprise_wechat.models import EnterpriseWechatUser


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    user_type = models.CharField(max_length=32)
    gender = models.CharField(max_length=4, default=0)
    avatar = models.CharField(max_length=1024, default="")
    mobile = models.CharField(max_length=32, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    enterprise_wechat_user = models.ForeignKey(EnterpriseWechatUser, default=None, on_delete=models.CASCADE)

    @property
    def wework_id(self):
        if self.enterprise_wechat_user:
            return self.enterprise_wechat_user.user_id
        return None
