from django.contrib import admin
from .models import EnterpriseWechatApp, EnterpriseWechatAccessToken, EnterpriseWechatUser


# Register your models here.
@admin.register(EnterpriseWechatApp)
class EnterpriseWechatAppAdmin(admin.ModelAdmin):
    list_display = ['pk', 'corp_id', 'agent_id', 'corp_secret', 'remark']


@admin.register(EnterpriseWechatAccessToken)
class EnterpriseWechatAccessTokenAdmin(admin.ModelAdmin):
    list_display = ["pk", "enterprise_wechat_app",
                    "access_token", "expire_in", "created"]


@admin.register(EnterpriseWechatUser)
class EnterpriseWechatUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'user_id', 'gender_name', 'mobile']

    def gender_name(self, item):
        names = {0: "unknown", 1: "male", 2: "female"}
        return names.get(item.gender)
