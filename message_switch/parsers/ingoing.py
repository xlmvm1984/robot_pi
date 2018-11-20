#!coding:utf8
import json
from . import BaseParser


class IngoingParser(BaseParser):

    def parse(self):
        data = json.loads(self.raw)
        return self._format(data)


parser = IngoingParser
name = "ingoing"
