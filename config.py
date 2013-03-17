# -*- coding: utf-8 -*-
import os
import re

APPID=os.environ.get('APPLICATION_ID')
APPID=re.sub(u'^s~',r'',APPID)
HOST="https://"+APPID+".appspot.com"
SENDER="snippets <snippets@"+APPID+".appspotmail.com>"
