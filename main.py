from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import pandas as pd
import requests
import json
from CreatePriceTable import CreatePriceTable


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('6bXHs/jPjVj0AF1omak6d+dDWo75sBBvdzDMlfdldmwn9kSDWAR7TKAcFvv3iqoEcUgHk6hlWZVWIbfOPmbuyyDcH9T3+fTB6pjU1TNwHN/gmVRIpXk/uV+rPxaw634q/R6BxtPUr79wHplnSnIn4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('718b8cd92bfb327982527e62b9b4f1c7')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    sent = message.split(' ')
    if sent[0] == '$':
        message = CreatePriceTable.create_price_table(message)
        FlexMessage = json.dumps(message)
    print(FlexMessage)
    #FlexMessage = json.load(open('FlexMessage.json', 'r', encoding='utf-8'))
    line_bot_api.reply_message(reply_token, FlexSendMessage('Price Table', FlexMessage))
    #line_bot_api.reply_message(reply_token, TextSendMessage(text = event.message.text))

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 80))
    #app.run(host='0.0.0.0', port=port)
    app.run()