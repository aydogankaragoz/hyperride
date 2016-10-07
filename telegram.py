import os
import requests


def _sendMessage(text):
    url = "https://api.telegram.org/bot" + os.environ['TELEGRAM_TOKEN'] + "/sendMessage"
    payload = {'chat_id': os.environ['TELEGRAM_CHAT_ID'],
               'text': text}
    r = requests.post(url, data=payload)


def newUser(firstname, city):
    text = u"{0} from {1} just joined.\n".format(firstname, city)
    _sendMessage(text)


def existingUser(firstname, city):
    text = u"{0} from {1} re-trying \n".format(firstname, city)
    _sendMessage(text)
