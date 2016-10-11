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


def newActivity(owner_id, object_id, event_time):
    text = u"New activity[{0}] by user[{1}] at: {2} \n".format(owner_id, object_id, event_time)
    _sendMessage(text)
