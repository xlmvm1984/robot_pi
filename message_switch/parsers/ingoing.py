#!coding:utf8
import json
from . import BaseParser


class IngoingParser(BaseParser):
    name = "ingoing"

    def parse(self):
        data = json.loads(self.raw)

