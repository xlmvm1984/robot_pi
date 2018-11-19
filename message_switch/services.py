#!coding:utf8
import json
from .models import RobotPi
from django.shortcuts import get_object_or_404
from enterprise_wechat.services import EnterpriseWechatSendMessageService
from user_mgmt.models import User


class RobotInboundService(object):
    robot = None
    data = None

    @classmethod
    def create(cls, uuid, data):
        obj = cls()
        obj.robot = get_object_or_404(RobotPi, uuid=uuid)
        obj.data = json.loads(data)
        return obj

    def _send_to_wework(self, user_id):
        service = EnterpriseWechatSendMessageService.create(self.robot.app_id)
        return service.send_card_msg(user_id, self.data.get("title"), self.data.get("text"),
                                     self.data.get("highlight"))

    def send(self):
        user = get_object_or_404(User, pk=self.robot.user_id)
        if user.wework_id != "":
            return self._send_to_wework(user.wework_id)
