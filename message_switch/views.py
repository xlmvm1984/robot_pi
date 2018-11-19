from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .services import RobotInboundService


# Create your views here.
class RobotInboundView(View):
    def get(self, request, uuid):
        return HttpResponse("uuid is ", uuid)

    def post(self, request, uuid):
        try:
            s = RobotInboundService.create(uuid, request.body)
            ret = s.send()
            return JsonResponse(ret)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"errcode": 999, "errmsg": str(e)})

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(RobotInboundView, self).dispatch(request, *args, **kwargs)
