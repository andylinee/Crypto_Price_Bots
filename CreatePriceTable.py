import json
import requests
import pandas as pd


class CreatePriceTable:
    def create_price_table(sentence):
        column = pd.DataFrame(columns=['Token', 'Price', '24HR', '7D', '30D'])
        token_list = sentence.split(' ')[1:]
        json_file = "FlexMessage.json"
        token_file = "TokenPrice.json"
        with open(json_file, 'r') as jf:
            FlexMessage = json.load(jf)
            #TokenPrice = json.load("TokenPrice.json")
            for i in range(len(token_list)):
                with open(token_file, 'r') as tp:
                    token = token_list[i]
                    print(token)
                    token_json = json.load(tp)
                    request_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+token+"&price_change_percentage=24h,7d,30d"
                    response = requests.get(request_url)
                    data = json.loads(response.text)
                    #values = list()
                    #values.append(token)
                    token_json["contents"][0]["contents"][0]["text"] = token
                    #values.append(data[0]['current_price'])
                    token_json["contents"][1]["text"] = data[0]['current_price']
                    #values.append("{0:.2f}%".format(data[0]['price_change_percentage_24h_in_currency']))
                    token_json["contents"][2]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_24h_in_currency'])
                    try:
                        #values.append("{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency']))
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency'])
                    except:
                        #values.append("Null")
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_7d_in_currency'])
                    try:
                        #values.append("{0:.2f}%".format(data[0]['price_change_percentage_30d_in_currency']))
                        token_json["contents"][4]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_30d_in_currency'])
                    except:
                        #values.append("Null")
                        token_json["contents"][4]["text"] = "{0:.2f}%".format(data[0]['price_change_percentage_30d_in_currency'])
                    #column.loc[i] = values
                    FlexMessage["body"]["contents"][1]["contents"].append(token_json)
                    tp.close()
        return FlexMessage