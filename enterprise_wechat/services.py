#!coding:utf8
from random import randint
from time import time
from .wework.CorpApi import CorpApi
from .wework.WXBizMsgCrypt import WXBizMsgCrypt, Prpcrypt
from .models import EnterpriseWechatApp
from django.shortcuts import get_object_or_404
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
    xml = ET.Element("xml")
    for key, val in json_obj.items():
        node = ET.SubElement(xml, key)
        node.text = str(val)
    msg = str(ET.tostring(xml), encoding="utf8")
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
            raise ValueError(msg)
        msg = xmltodict.parse(msg)
        msg = dict(msg).get("xml")
        return msg

    def encrpty_msg(self, msg, nonce):
        msg = json2xml_2(msg)
        ret, msg_encrpty = self.wxcpt.EncryptMsg(msg, nonce)
        msg = json2xml(json.loads(msg_encrpty))
        return msg


class EnterpriseWechatReplyMessageService(object):
    msg_recv = None
    app = None
    enterprise_wechat_service = None

    @classmethod
    def create(cls, app_id, signature, ts, nonce, data):
        obj = cls()
        obj.app = get_object_or_404(EnterpriseWechatApp, pk=app_id)
        obj.enterprise_wechat_service = EnterpriseWechatService.create(obj.app)
        obj.msg_recv = obj.enterprise_wechat_service.decrpty_msg(signature=signature, ts=ts, nonce=nonce, data=data)
        return obj

    def echo(self):
        msg = self.msg_recv
        msg = {
            "ToUserName": msg.get("FromUserName"), "FromUserName": msg.get("FromUserName"),
            "CreateTime": int(time()), "MsgType": "text", "Content": msg.get("Content"),
            "MsgId": msg.get("MsgId"), "AgentID": msg.get("AgentID")
        }
        msg = self.enterprise_wechat_service.encrpty_msg(msg, str(randint(1000000000, 9000000000)))
        return msg
