from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .services import EnterpriseWechatService
from .models import EnterpriseWechatApp

# Create your views here.


class MessageVerifyView(View):
    def get(self, request, app_id):
        query_string = request.GET
        signature, echostr, nonce, ts = query_string.get("signature"), query_string.get("echostr"),\
                                        query_string.get("nonce"), query_string.get("timestamp")
        app = get_object_or_404(EnterpriseWechatApp, pk=app_id)
        enterprise_wechat_service = EnterpriseWechatService.create(app)
        echo_msg = enterprise_wechat_service.verify_url(signature, echostr, nonce, ts)
        return HttpResponse(echo_msg)
