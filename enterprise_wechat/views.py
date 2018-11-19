from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .services import EnterpriseWechatService, EnterpriseWechatReplyMessageService
from .models import EnterpriseWechatApp


# Create your views here.


class MessageVerifyView(View):
    def get(self, request, app_id):
        query_string = request.GET
        signature, echostr, nonce, ts = query_string.get("msg_signature"), query_string.get("echostr"),
        query_string.get("nonce"), query_string.get("timestamp")
        app = get_object_or_404(EnterpriseWechatApp, pk=app_id)
        enterprise_wechat_service = EnterpriseWechatService.create(app)
        echo_msg = enterprise_wechat_service.verify_url(
            ts=ts, nonce=nonce, echostr=echostr, signature=signature)
        return HttpResponse(echo_msg)

    def post(self, request, app_id):
        query_string = request.GET
        signature, nonce, ts = query_string.get("msg_signature"), query_string.get("nonce"),\
            query_string.get("timestamp")
        reply_message_service = EnterpriseWechatReplyMessageService.create(app_id=app_id, signature=signature, ts=ts,
                                                                           nonce=nonce, data=request.body)
        return HttpResponse(reply_message_service.echo())

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MessageVerifyView, self).dispatch(*args, **kwargs)
