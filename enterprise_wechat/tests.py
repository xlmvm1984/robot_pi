import base64
from django.test import TestCase
from uuid import uuid1

from .models import EnterpriseWechatApp, EnterpriseWechatUser
from .services import EnterpriseWechatService, EnterpriseWechatUserService
from .wework.WXBizMsgCrypt import Prpcrypt


class BaseTests(TestCase):
    def setUp(self):
        self.app = EnterpriseWechatApp(corp_id="ww45ddb2f96a6d8069",
                                       corp_secret="UOMhJgyIPWwCThXDocptwFUshz4WlfkIyeQPSouvPBQ",
                                       agent_id="1000002",
                                       message_token="pNyHjGopPiwyTkRo",
                                       message_aes_key="THBjcgz75TBLMPizigJkarLYtHFP5DfwYW1pcxmJ9oE",
                                       )
        self.app.save()


class EnterpriseWechatServiceTests(BaseTests):
    def setUp(self):
        super(EnterpriseWechatServiceTests, self).setUp()
        self.enterprise_wechat_service = EnterpriseWechatService.create(self.app)

    def test_fetch_accesss_token(self):
        self.assertIsNotNone(self.enterprise_wechat_service.core_api._token)
        self.assertIsNotNone(
            self.enterprise_wechat_service.core_api.access_token)

    def test_encrption_decryption(self):
        prp = Prpcrypt(base64.b64decode(self.app.message_aes_key + "="))
        random_str = str(uuid1())
        ret, encrpty_str = prp.encrypt(random_str, self.app.corp_id)
        self.assertIs(ret, 0)
        print("encrpty_str is ", encrpty_str)
        ret, decrpty_str = prp.decrypt(encrpty_str, self.app.corp_id)
        self.assertIs(ret, 0)
        print("decrpty_str is ", decrpty_str)
        self.assertEqual(decrpty_str, random_str)


class EnterpriseWechatUserServiceTests(BaseTests):
    def setUp(self):
        super(EnterpriseWechatUserServiceTests, self).setUp()
        self.user_service = EnterpriseWechatUserService.create(self.app.pk)

    def test_fetch_user_and_save(self):
        user_id = "LiangYejin"
        user = self.user_service.fetch_user(user_id)
        print(user)
        self.assertIsNotNone(user)
        user_saved = EnterpriseWechatUser.objects.get(user_id=user_id)
        self.assertEqual(user, user_saved)
