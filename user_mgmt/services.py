#!coding:utf8

from enterprise_wechat.models import EnterpriseWechatUser
from .models import User


class UserService(object):
    @classmethod
    def create(cls):
        obj = cls()
        return obj

    # once we fetch or get a user info from wework, save or update it in users
    def create_or_update_user_from_wework(self, enterprise_wechat_user):
        defaults = {"name": enterprise_wechat_user.name, "gender": enterprise_wechat_user.gender,
                    "mobile": enterprise_wechat_user.mobile, "avatar": enterprise_wechat_user.avatar}
        obj, created = User.objects.update_or_create(enterprise_wechat_user=enterprise_wechat_user, defaults=defaults)
        return obj
