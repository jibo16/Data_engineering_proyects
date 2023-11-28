import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, CURR_, P_PHONE
import time
import json
import pandas as pd
import requests
from tqdm import tqdm

req = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key={}".format(CURR_))


## Json to values and conversion to mxn for each currency
Rates = req.json()['rates']
mxn = Rates['MXN']
def convertor(rates, i):
    if i != 'MXN':
        return currency_list[i], mxn/rates[i]
    return currency_list[i], rates[i]
currency_list = {'USD':'Dolar de EEUU','MXN':'Euro', 'GBP':'Libra Ingles', 'JPY':'Yuan Japones', 'AUD':'Dolar Australiano', 'CAD': 'Dolar Canadiense', 'CHF':'Franco Suizo' , 'BTC':'Bitcoin', 'CNY':'Yuan Chino'}

## Creates the message
msg_main = ""
for i in tqdm(currency_list.keys()):
    mon, pre = convertor(Rates,i)
    row_msg = '{}: {}'.format(mon,round(pre,2))
    msg_main+= '\n' + row_msg + '\n'

## Sends the message
time.sleep(.5)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid,auth_token)
message = client.messages \
                .create(
                    body = msg_main,
                    from_=PHONE_NUMBER,
                    to= P_PHONE
                )
print('Mensaje enviado' + message.sid)
