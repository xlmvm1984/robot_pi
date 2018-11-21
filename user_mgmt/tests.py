from django.test import TestCase
from enterprise_wechat.services import EnterpriseWechatUserService, EnterpriseWechatApp
from .services import UserService
from .models import User

# Create your tests here.
class UserServiceTests(TestCase):
    def setUp(self):
        self.app = EnterpriseWechatApp(corp_id="ww45ddb2f96a6d8069",
                                       corp_secret="UOMhJgyIPWwCThXDocptwFUshz4WlfkIyeQPSouvPBQ",
                                       agent_id="1000002",
                                       message_token="pNyHjGopPiwyTkRo",
                                       message_aes_key="THBjcgz75TBLMPizigJkarLYtHFP5DfwYW1pcxmJ9oE",
                                       )
        self.test_user_id = "LiangYejin"
        self.app.save()

    def test_fetch_wechat_auto_create_user(self):
        enterprise_wechat_user_service = EnterpriseWechatUserService.create(self.app.pk)
        wework_user = enterprise_wechat_user_service.fetch_user(self.test_user_id)
        service = UserService.create()
        user = service.create_or_update_user_from_wework(enterprise_wechat_user=wework_user)
        # check if user created
        self.assertEqual(user.mobile, wework_user.mobile)
        user.mobile ="9999912340"
        user.save()
        count = user.objects.count()

        # check if mobile is not same
        self.assertNotEqual(user.mobile, wework_user.mobile)
        user = service.create_or_update_user_from_wework(wework_user)

        # check if mobile is same after update
        self.assertEqual(user.mobile, wework_user.mobile)

        # check if no new record created
        self.assertEqual(count, user.objects.count())
