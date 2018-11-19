import urllib
import json
import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .services import EnterpriseWechatService
from .models import EnterpriseWechatApp


# Create your views here.


class MessageVerifyView(View):
    def get(self, request, app_id):
        query_string = request.GET
        _ = (signature, echostr, nonce, ts) = (query_string.get("msg_signature"), query_string.get("echostr"),\
                                        query_string.get("nonce"), query_string.get("timestamp"))
        app = get_object_or_404(EnterpriseWechatApp, pk=app_id)
        enterprise_wechat_service = EnterpriseWechatService.create(app)
        echo_msg = enterprise_wechat_service.verify_url(ts=ts, nonce=nonce, echostr=echostr, signature=signature)
        return HttpResponse(echo_msg)


    def post(self, request, app_id):
        print("POSTED ", str(request.body))
        query_string = request.GET
        signature, nonce, ts = query_string.get("msg_signature"), query_string.get("nonce"),\
                               query_string.get("timestamp")
        app = get_object_or_404(EnterpriseWechatApp, pk=app_id)
        enterprise_wechat_service = EnterpriseWechatService.create(app)
        msg = enterprise_wechat_service.decrpty_msg(signature=signature, ts=ts, nonce=nonce, data=request.body)
        print("=====message found : ", msg)
        msg_str = json.dumps({
            "ToUserName": msg.get("FromUserName"), "FromUserName": msg.get("FromUserName"),
            "CreateTime": int(time.time()), "MsgType": "text", "Content": msg.get("Content"), "MsgId": msg.get("MsgId"),
            "AgentID": msg.get("AgentID")
        })
        msg = enterprise_wechat_service.encrpty_msg(msg, nonce)
        print("===="*20)
        print(msg)
        return HttpResponse(msg)
        # Todo

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MessageVerifyView, self).dispatch(*args, **kwargs)
