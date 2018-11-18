from django.test import TestCase
from .models import EnterpriseWechatAccessToken, EnterpriseWechatApp
from .services import EnterpriseWechatService
from .wework.CorpApi import CorpApi


# Create your tests here.
class EnterpriseWechatServiceTests(TestCase):
    def setUp(self):
        self.app = EnterpriseWechatApp(corp_id="ww45ddb2f96a6d8069",
                                       corp_secret="UOMhJgyIPWwCThXDocptwFUshz4WlfkIyeQPSouvPBQ",
                                       agent_id="1000002")
        self.app.save()
        self.enterprise_wechat_service = EnterpriseWechatService.create(self.app)

    def test_fetch_accesss_token(self):
        self.assertIsNotNone(self.enterprise_wechat_service.core_api._token)
        self.assertIsNotNone(self.enterprise_wechat_service.core_api.access_token)
