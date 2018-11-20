#!coding:utf8
"""
Parser of Webhook from github
Supported Event Type:
- ping
- push

"""
import json
from . import BaseParser

__version__ = 0.1


class GithubParser(BaseParser):
    event = None
    payload = None

    def parse(self):
        self.payload = json.loads(self.raw)
        self.event = self.get_event()
        action = "_%s_parser" % self.event
        data = getattr(self, action)()
        return self._format(data)

    def get_event(self):
        return self.headers.get("X-GitHub-Event")

    def _ping_parser(self):
        hook = self.payload.get("hook")
        ret = {"title": "Webhook %s has been setup." % hook.get("name"), "highlight": "active: %s" % hook.get("active"),
               "url": hook.get("url")}
        return ret

    def _push_parser(self):
        title = "% pushed to %s" % (self.payload.get("pusher").get("name"), self.payload.get("repostory").get("name"))
        text = "".join(["<p>%s</p>" for r in self.payload.get("commits")])
        url = self.payload.get("compare")
        return dict(title=title, url=url, text=text)


parser = GithubParser
name = "github"