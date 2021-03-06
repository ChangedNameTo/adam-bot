import os
import random
from flask import Flask, json, request
import requests
import re
import time

app = Flask(__name__)

lastTime = -3600

def reply(message):
    print("Replying to group")
    payload = {
        'bot_id'      : os.environ['BOT_ID'],
        'text'        : message,
        'attachments' : [
                {
                        'type' : 'image',
                        'url'  : 'https://i.groupme.com/368x368.gif.0ddac4592b7840ca9bc78adf619ac928'
                        }
                ]
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=payload)


@app.route('/', methods=['POST','GET'])
def groupme_callback():
    global lastTime
    print("Got Connection...parsing:")
    json_body = request.get_json()
    if json_body['group_id'] == os.environ['GROUP_ID'] and json_body['sender_type'] != 'bot':
        # some degree of verification that it is sent via a groupme callback
        # could also check for "User-Agent: GroupMeBotNotifier/1.0", but that's plenty spoofable

        message = json_body['text']
        if any(adam in message.lower().split() + json_body['name'].lower().split() for adam in ["adam", "@adam"]) and time.clock() - lastTime > 3600:
                lastTime = time.clock()
                print("Adam found!")
                reply("Adam!")
        else:
                print("Adam Not Found in: {}".format(message))
    else:
        print("Not from groupme!")
    return "ok", 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port)
