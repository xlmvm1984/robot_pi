#!coding:utf8
import json


class BaseParser(object):
    raw = None

    @classmethod
    def create(cls, data, headers=None):
        _data = data if isinstance(data, str) else str(data, encoding="utf8")
        obj = cls()
        obj.raw = _data
        obj.headers = headers
        return obj

    def parse(self):
        raise NotImplementedError

    def _format(self, data):
        return {"url": data.get("url"), "text": data.get("text"), "title": data.get("title"),
                "highlight": data.get("highlight")}
