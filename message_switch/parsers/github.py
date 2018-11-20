#!coding:utf8
"""
Parser of Webhook from github
Supported Event Type:
- ping
- push
"""
import json
from . import BaseParser, ParserError

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
        data["title"]="GitHub: %s" % self.repository.get("name") if self.repository else None
        data["highlight"] = "%s: %s" % (self.sender.get("login"), self.event.replace("_", " "))
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
        ref = self.payload.get("ref")
        branch = ref.split("/")[-1]
        if not branch == "master":
            raise ParserError("Not on master branch, droped")

        text = "\n".join(["- %s" % r.get("message") for r in self.payload.get("commits")])
        url = self.payload.get("compare")
        return dict(url=url, text=text)

    def _pull_request_review_comment_parser(self):
        action = self.payload.get("action")
        comment = self.payload.get("comment")
        text = "[%s]%s: %s" % (action, comment.get("user").get("login"), comment.get("body"))
        url = comment.get("url")
        return dict(url=url, text=text)

    def _pull_request_parser(self):
        pr = self.payload.get("pull_request")
        text = "Pull request: '%s' is %s\ncontent: %s" % (pr.get("title"), self.payload.get("action"), pr.get("body"))
        url = pr.get("html_url")
        return dict(url=url, text=text)


parser = GithubParser
name = "github"
