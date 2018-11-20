#!coding:utf8
import json
import os
import importlib
from .models import RobotPi
from django.shortcuts import get_object_or_404
from enterprise_wechat.services import EnterpriseWechatSendMessageService
from user_mgmt.models import User
from robot_pi.settings import DEFAULT_WEWORK_URL
from .parsers import ParserError


def import_parsers():
    parsers_dir = os.path.join(os.path.dirname(__file__), "parsers")
    supported_parsers = {}
    files = filter(lambda x: x.endswith(".py") and not x.startswith("_"), os.listdir(parsers_dir))
    for file in files:
        mod_name = ".parsers."+file.replace(".py", "")
        mod = importlib.import_module(mod_name, __package__)
        supported_parsers[mod.name] = mod.parser
    return supported_parsers

supported_parsers = import_parsers()


class RobotInboundService(object):
    robot = None
    data = None
    headers = None
    error_msg = None

    @classmethod
    def create(cls, uuid, data, headers=None):
        obj = cls()
        obj.robot = get_object_or_404(RobotPi, uuid=uuid)
        parser = supported_parsers[obj.robot.type_name].create(data, headers)
        try:
            obj.data = parser.parse()
            obj.headers = headers  # some webhook put infomation in headers
        except ParserError as e:
            obj.error_msg = e.args[0]
        return obj

    def _send_to_wework(self, user_id):
        service = EnterpriseWechatSendMessageService.create(self.robot.app_id)
        return service.send_card_msg(user_id, self.data.get("title"), self.data.get("text"),
                                     self.data.get("highlight"), self.data.get("url") or DEFAULT_WEWORK_URL)

    def send(self):
        user = get_object_or_404(User, pk=self.robot.user_id)
        if not self.data:
            # nothing to send
            return self.error_msg or "Nothing to send"
        if user.wework_id != "":
            return self._send_to_wework(user.wework_id)
