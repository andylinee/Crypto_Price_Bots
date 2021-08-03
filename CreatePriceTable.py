import json
import requests
import pandas as pd

# Token List
SBF_list = ['ftx-token', 'serum', 'solana', 'bonfida', 'maps', 'raydium', 'oxygen', 'sushi']
platform_list = ['binancecoin', 'ftx-token', 'okb', 'huobi-token']

# Reference Files
json_file = "FlexMessage.json"
token_file = "TokenPrice.json"

class CreatePriceTable:
    def get_token_price_table(sentence):
        """ Return User-typed Token Price Table """
        token_list = sentence.split(' ')[1:]
        with open(json_file, 'r') as jf:
            FlexMessage = json.load(jf)
            print(FlexMessage)
            if token_list[0] == "SBF":
                token_list = SBF_list
                FlexMessage["header"]["contents"][0]["text"] = 'SBF Token'
            elif token_list[0] == "Platform":
                token_list = platform_list
                FlexMessage["header"]["contents"][0]["text"] = 'Platform Token'
            for i in range(len(token_list)):
                with open(token_file, 'r') as tp:
                    token = token_list[i]
                    print(token)
                    token_json = json.load(tp)
                    print(token_json)
                    request_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+token+"&price_change_percentage=24h,7d"
                    response = requests.get(request_url)
                    data = json.loads(response.text)
                    token_json["contents"][0]["text"] = data[0]['symbol'].upper() + " (" + data[0]['name'] + ")"
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

    def get_top_token_price_table(sentence):
        """ Return Top-n Token Price Table """
        num_top = sentence.split(' ')[2]
        json_file = "FlexMessage.json"
        token_file = "TokenPrice.json"
        with open(json_file, 'r') as jf:
            FlexMessage = json.load(jf)
            #print(FlexMessage)
            FlexMessage["header"]["contents"][0]["text"] = 'Top ' + str(num_top) + ' Token'
            request_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=" + num_top + "&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d"
            response = requests.get(request_url)
            data = json.loads(response.text)
            for i in range(int(num_top)):
                with open(token_file, 'r') as tp:
                    token_json = json.load(tp)
                    print(token_json)
                    token_json["contents"][0]["text"] = data[i]['symbol'].upper() + " (" + data[i]['name'] + ")"
                    token_json["contents"][1]["text"] = str(data[i]['current_price'])
                    token_json["contents"][2]["text"] = "{0:.2f}%".format(data[i]['price_change_percentage_24h_in_currency'])
                    try:
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[i]['price_change_percentage_7d_in_currency'])
                    except:
                        token_json["contents"][3]["text"] = "{0:.2f}%".format(data[i]['price_change_percentage_7d_in_currency'])
                    FlexMessage["body"]["contents"][0]["contents"].append(token_json)
                    print("-" * 30)
                    print(token_json)
                    tp.close()
                jf.close()
        return FlexMessage
    
    def get_commands_list():
        """ Return Commands List """
        json_file = "CmdFlexMessage.json"
        cmd_file = "CommandsList.json"
        cmdDict = {
            "$ <token_id>": "One token price",
            "$ <tid1> <tid2> ...": "Many tokens price",
            "$ Top <num>": "Top <num> tokens",
            "$ SBF": "SBF-series tokens",
            "$ Platform": "Platform tokens"}
        with open(json_file, 'r') as jf:
            FlexMessage = json.load(jf)
            for cmd, desc in cmdDict.items():
                with open(cmd_file, 'r') as cp:
                    cmd_json = json.load(cp)
                    cmd_json["contents"][0]["text"] = cmd
                    cmd_json["contents"][1]["text"] = desc
                    FlexMessage["body"]["contents"][0]["contents"].append(cmd_json)
                    cp.close()
                jf.close()
        return FlexMessage