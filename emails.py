# -*- coding: utf-8 -*-
import logging

from google.appengine.api import mail
from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from dateutil import *
from model import *

REMINDER = """
한 주간 수고하셨습니다.
회신으로 업무내역을 입력해주세요. :)

지난주 한 일
- 

이번주 할 일
- 
"""

class ReminderEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            # TODO: Check if one has already been submitted for this period.
            taskqueue.add(url='/onereminder', params={'email': user.email})


class OneReminderEmail(webapp.RequestHandler):
    def post(self):
        mail.send_mail(sender="snippets <snippets@minisnippets.appspotmail.com>", # FIX ME
                       to=self.request.get('email'),
                       subject="Snippet 타임!",
                       body=REMINDER)

    def get(self):
        post(self)

class DigestEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            taskqueue.add(url='/onedigest', params={'email': user.email})
            

class OneDigestEmail(webapp.RequestHandler):
    def __send_mail(self, recipient, body):
        mail.send_mail(sender="snippets <snippets@minisnippets.appspotmail.com>", # FIX ME
                       to=recipient,
                       subject="Snippet Digest 메일이 도착하였습니다!",
                       body=body)

    def __snippet_to_text(self, snippet):
        divider = '-' * 30
        return '%s\n%s\n%s' % (snippet.user.pretty_name(), divider, snippet.text)

    def get(self):
        post(self)

    def post(self):
        user = user_from_email(self.request.get('email'))
        d = date_for_retrieval()
        all_snippets = Snippet.all().filter("date =", d).fetch(500)
        all_users = User.all().fetch(500)
        following = compute_following(user, all_users)
        logging.info(all_snippets)
        body = '\n\n\n'.join([self.__snippet_to_text(s) for s in all_snippets if s.user.email in following])
        if body:
            self.__send_mail(user.email, 'https://minisnippets.appspot.com\n\n' + body) # FIX ME
        else:
            logging.info(user.email + ' not following anybody.')
