#!coding:utf8
from .wework.CorpApi import CorpApi
from .wework.WXBizMsgCrypt import WXBizMsgCrypt


class EnterpriseWechatService(object):
    app = None
    core_api = None

    @classmethod
    def create(cls, app, _auto_load_core_api=True):
        obj = cls()
        cls.app = app
        if _auto_load_core_api is True:
            core_api = CorpApi(app)
            core_api.refreshAccessToken()
            obj.core_api = core_api
        return obj


    def verify_url(self, signature, ts, nonce, echostr):
        # decrpto echostr & return msg
        wxcpt = WXBizMsgCrypt(self.app.message_token, self.app.message_aes_key, self.app.corp_id)
        ret, echo_msg = wxcpt.VerifyURL(signature, ts, nonce, echostr)
        if ret == 0:
            return echo_msg
        else:
            return "error: %s" % ret
