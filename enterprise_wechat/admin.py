from django.contrib import admin
from .models import EnterpriseWechatApp, EnterpriseWechatAccessToken


# Register your models here.
@admin.register(EnterpriseWechatApp)
class EnterpriseWechatAppAdmin(admin.ModelAdmin):
    list_display = ['pk', 'corp_id', 'agent_id', 'corp_secret', 'remark']


@admin.register(EnterpriseWechatAccessToken)
class EnterpriseWechatAccessTokenAdmin(admin.ModelAdmin):
    list_display = ["pk", "enterprise_wechat_app", "access_token", "expire_in", "created"]