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
        message = price_table(message)
    FlexMessage = json.load(open('FlexMessage.json', 'r', encoding='utf-8'))
    line_bot_api.reply_message(reply_token, FlexSendMessage('Price Table', FlexMessage))
    #line_bot_api.reply_message(reply_token, TextSendMessage(text = event.message.text))

def price_table(sentence):
    column = pd.DataFrame(columns=['Token', 'Price', '24HR', '7D', '30D'])
    token_list = sentence.split(' ')[1:]
    #print(token_list)
    for i in range(len(token_list)):
        token = token_list[i]
        print(token)
        request_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+token+"&price_change_percentage=24h,7d,30d"
        response = requests.get(request_url)
        data = json.loads(response.text)
        values = list()
        values.append(token)
        values.append(data[0]['current_price'])
        values.append("{0:.2f}%".format(data[0]['price_change_percentage_24h_in_currency']))
        try:
            values.append("{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency']))
        except:
            values.append("Null")
        try:
            values.append("{0:.2f}%".format(data[0]['price_change_percentage_30d_in_currency']))
        except:
            values.append("Null")
        column.loc[i] = values
    print(column)
    return column

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 80))
    #app.run(host='0.0.0.0', port=port)
    app.run()