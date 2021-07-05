from flask import Flask, request, abort
import settings
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from CreatePriceTable import CreatePriceTable
import pandas as pd
import requests
import json


app = Flask(__name__)
# LINE BOT info Settings
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    sent = message.split(' ')
    if sent[0] == '$':
        if sent[1] == "top":
            flex_message = CreatePriceTable.top_token_list(message)
            line_bot_api.reply_message(reply_token, FlexSendMessage('Top Token List', flex_message))
        else:
            flex_message = CreatePriceTable.create_price_table(message)
            line_bot_api.reply_message(reply_token, FlexSendMessage('Price Table', flex_message))
    
    #line_bot_api.reply_message(reply_token, TextSendMessage(text = event.message.text))

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 80))
    #app.run(host='0.0.0.0', port=port)
    app.run()