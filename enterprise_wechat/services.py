#!coding:utf8
from .wework.CorpApi import CorpApi
from .wework.WXBizMsgCrypt import WXBizMsgCrypt


class EnterpriseWechatService(object):
    app = None
    core_api = None

    @classmethod
    def create(cls, app):
        obj = cls()
        cls.app = app
        core_api = CorpApi(app)
        core_api.refreshAccessToken()
        obj.core_api = core_api
        self.wxcpt = WXBizMsgCrypt(self.app.message_token, self.app.message_aes_key, self.app.corp_id)
        return obj

    def verify_url(self, signature, ts, nonce, echostr):
        # decrpto echostr & return msg
        ret, echo_msg = self.wxcpt.VerifyURL(signature, ts, nonce, echostr)
        if ret == 0:
            return echo_msg
        else:
            return "error: %s" % ret

    def decrpty_msg(self, signature, ts, nonce, data):
        ret, msg = self.wxcpt.DecryptMsg(data, signature, ts, nonce)
        if ret != 0:
            raise ValueError(msg)
        return msg

    def encrpty_msg(self, msg, nonce):
        wxcpt = WXBizMsgCrypt(self.app.message_token, self.app.message_aes_key, self.app.corp_id)
        ret, msg_encrpty = wxcpt.EncryptMsg(msg, nonce)
        return msg_encrpty

