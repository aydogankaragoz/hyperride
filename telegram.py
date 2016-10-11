import os
import requests


def _sendMessage(text):
    url = "https://api.telegram.org/bot" + os.environ['TELEGRAM_TOKEN'] + "/sendMessage"
    payload = {'chat_id': os.environ['TELEGRAM_CHAT_ID'],
               'text': text}
    r = requests.post(url, data=payload)


def newUser(firstname, lastname):
    text = u"{0} {1} just joined.\n".format(firstname, lastname)
    _sendMessage(text)


def existingUser(firstname, lastname):
    text = u"{0} {1} re-trying \n".format(firstname, lastname)
    _sendMessage(text)


def newActivity(firstname, lastname, activity):
    text = u"New activity by {0} {1}, activity id=  {2} \n".format(firstname, lastname, activity)
    _sendMessage(text)
