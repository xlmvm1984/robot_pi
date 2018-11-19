#!coding:utf8


class BaseParser(object):
    name = None
    raw = None

    @classmethod
    def create(cls, data):
        if isinstance(data, bytes):
            _data = str(data, encoding="utf8")
        else:
            _data = data
        obj = cls()
        obj.raw = obj

    def parse(self):
        raise NotImplementedError

    def _format(self, data):
        """:return {"title": TITLE, "text": TEXT, ""}"""
