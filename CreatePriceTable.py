import json
import requests
import pandas as pd


class CreatePriceTable:
    def create_price_table(sentence):
        token_list = sentence.split(' ')[1:]
        json_file = "FlexMessage.json"
        token_file = "TokenPrice.json"
        with open(json_file, 'r') as jf:
            FlexMessage = json.load(jf)
            print(FlexMessage)
            #TokenPrice = json.load("TokenPrice.json")
            for i in range(len(token_list)):
                with open(token_file, 'r') as tp:
                    token = token_list[i]
                    print(token)
                    token_json = json.load(tp)
                    print(token_json)
                    request_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+token+"&price_change_percentage=24h,7d"
                    response = requests.get(request_url)
                    data = json.loads(response.text)
                    token_json["contents"][0]["text"] = token
                    token_json["contents"][1]["text"] = str(data[0]['current_price'])
                    token_json["contents"][2]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_24h_in_currency'])
                    try:
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency'])
                    except:
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency'])
                    FlexMessage["body"]["contents"][0]["contents"].append(token_json)
                    print("-" * 30)
                    print(token_json)
                    tp.close()
                jf.close()
        return FlexMessage