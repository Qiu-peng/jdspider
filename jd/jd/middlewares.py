# -*- coding: utf-8 -*-

from jd.settings import USER_AGENTS
import random

class RandomUserAgentMiddleware(object):
    def process_request(self,request,spider):
        USER_AGENT = random.choice(USER_AGENTS)
        print(USER_AGENT)
        request.headers.setdefault('User-Agent',USER_AGENT)
