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
    repository = None
    sender = None

    def parse(self):
        self.payload = json.loads(self.raw)
        self.event = self.get_event()
        self.repository = self.payload.get("repository")
        self.sender = self.payload.get("sender")
        action = "_%s_parser" % self.event
        data = getattr(self, action)()
        data.update(title="GitHub RobotPi")
        data.update(highlight="Repository: %s" % self.repository.get("name"))
        return self._format(data)

    def get_event(self):
        return self.headers.get("HTTP_X_GITHUB_EVENT")

    def _ping_parser(self):
        hook = self.payload.get("hook")
        ret = {
            "text": "webhook setup, events: %s" % ",".join(hook.get("events")),
            "url": self.payload.get("repository").get("html_url")
        }
        return ret

    def _push_parser(self):
        text = "<p>% pushed</p>" % self.payload.get("pusher").get("name")
        text += "".join(["<p>%s</p>" for r in self.payload.get("commits")])
        url = self.payload.get("compare")
        return dict(title=title, url=url, text=text)


parser = GithubParser
name = "github"
