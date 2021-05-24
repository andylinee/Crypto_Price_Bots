import json
import requests
import pandas as pd


class CreatePriceTable:
    def create_price_table(sentence):
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
        return FlexMessage