import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_WAPI, P_PHONE
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm
import numpy as np

request_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WAPI}&q=mexico city&days=1&aqi=no&alerts=no"
response = requests.get(request_url).json()

def get_forecast(response, i):
    fecha = response["forecast"]["forecastday"][0]["hour"][i]['time'].split()[0]
    hora = int(response["forecast"]["forecastday"][0]["hour"][i]['time'].split()[1].split(':')[0])
    condicion = response["forecast"]["forecastday"][0]["hour"][i]['condition']['text']
    temperatura = response["forecast"]["forecastday"][0]["hour"][i]['temp_c']
    rain = response["forecast"]["forecastday"][0]["hour"][i]['will_it_rain']
    prob_rain = response["forecast"]["forecastday"][0]["hour"][i]['chance_of_rain']
    
    return fecha, hora, condicion, temperatura, rain, prob_rain


datos = []

for i in tqdm(range( len(response["forecast"]["forecastday"][0]["hour"])), colour ="purple"):
    datos.append(get_forecast(response, i))


cols = ['fecha', 'hora', 'condicion', 'temperatura', 'lluvia', 'prob_lluvia']
df = pd.DataFrame(datos,columns = cols)

msg = f'\n \n El pronostico del tiempo hoy a las {df["hora"][15]} es de {df["condicion"][15]}'

time.sleep(2)
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid,auth_token)
message = client.messages \
                .create(
                    body = msg,
                    from_=PHONE_NUMBER,
                    to= P_PHONE
                )
print('Mensaje enviado' + message.sid)