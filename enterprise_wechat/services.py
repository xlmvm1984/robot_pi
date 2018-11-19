#!coding:utf8
from .wework.CorpApi import CorpApi
from .wework.WXBizMsgCrypt import WXBizMsgCrypt, Prpcrypt
import xml.etree.cElementTree as ET
import json
import xmltodict


def xml2json(xml_str):
    xml_tree = ET.fromstring(xml_str)
    encrpty = xml_tree.find("Encrypt")
    return json.dumps({"Encrypt": encrpty.text})


def json2xml(json_obj):
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
  <Encrypt><![CDATA[%(Encrypt)s]]></Encrypt>
  <MsgSignature><![CDATA[%(MsgSignature)s]]></MsgSignature>
  <TimeStamp>%(TimeStamp)s</TimeStamp>
  <Nonce><![CDATA[%(Nonce)s]]></Nonce>
</xml>"""
    return AES_TEXT_RESPONSE_TEMPLATE % json_obj


def json2xml_2(json_obj):
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
<FromUserName><![CDATA[%(FromUserName)s]]></FromUserName>
<CreateTime>%(CreateTime)s</CreateTime>
<MsgType><![CDATA[%(MsgType)s]]></MsgType>
<Content><![CDATA[%(Content)s]]></Content>
<MsgId>%(MsgId)s</MsgId>
<AgentID>%(AgentID)s</AgentID>
</xml>"""
    msg = AES_TEXT_RESPONSE_TEMPLATE % json_obj
    msg = msg.replace("\n", "")
    return msg





class EnterpriseWechatService(object):
    app = None
    core_api = None

    @classmethod
    def create(cls, app):
        obj = cls()
        obj.app = app
        core_api = CorpApi(app)
        core_api.refreshAccessToken()
        obj.core_api = core_api
        obj.wxcpt = WXBizMsgCrypt(obj.app.message_token, obj.app.message_aes_key, obj.app.corp_id)
        return obj

    def verify_url(self, signature, ts, nonce, echostr):
        # decrpto echostr & return msg
        ret, echo_msg = self.wxcpt.VerifyURL(signature, ts, nonce, echostr)
        if ret == 0:
            return echo_msg
        else:
            return "error: %s" % ret

    def decrpty_msg(self, signature, ts, nonce, data):
        data = xml2json(data)
        ret, msg = self.wxcpt.DecryptMsg(data, signature, ts, nonce)
        if ret != 0:
            print(msg)
            raise ValueError(msg)
        print(msg)
        msg = xmltodict.parse(msg)
        msg = dict(msg).get("xml")
        return msg

    def encrpty_msg(self, msg, nonce):
        print("origin msg", msg)
        msg = json2xml_2(msg)
        print("before encrpty", msg)
        ret, msg_encrpty = self.wxcpt.EncryptMsg(msg, nonce)
        print(msg_encrpty)
        msg = json2xml(json.loads(msg_encrpty))
        pc = Prpcrypt(self.wxcpt.key)
        print("---"*10)
        print(pc.decrypt(msg_encrpty, self.wxcpt.m_sReceiveId))
        print("---"*10)
        return msg
