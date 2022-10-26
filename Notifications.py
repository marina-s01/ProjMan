#!/usr/bin/env python
# coding: utf-8

# In[2]:


import schedule #необходимо установить библиотеку
import time
import pandas as pd
import requests as req
import json
from geopy import geocoders
from geopy.geocoders import Nominatim
import telebot;
from telebot import types

bot = telebot.TeleBot('5688775484:AAFfcMbAm_t-qEOnuqanR63ivL4UJ-qJdeY') #переменная для работы с ботом через токен\
token_accu="7pNet2S89J6HC7m6DdPIh5beY93ZhPOS" #  токены: GuL1TlbAFOb3BDTnqE88YwIWmHXyhXCn    7pNet2S89J6HC7m6DdPIh5beY93ZhPOS    o8bQ6kOLDIm242Z9wZqvderTlzk6ynVR
df=pd.read_excel('./ntfDB.xlsx') # датафрейм, который считывает таблицу эксель с данными пользователей, которые включили уведомления и выбрали время, содержит три столбца: id чата, время отправки уведомления, город пользователя
print(df)

def geo_pos(city: str): #получение координат через название города
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude

def code_location(latitude: str, longitude: str, token_accu: str): #код города через accuweather при помощи коор-ат
    url_location_key = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={token_accu}&q={latitude},{longitude}&language=ru'
    resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    code = json_data['Key']
    return code

def weather_day(cod_loc: str, token_accu: str):
    day=0
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{cod_loc}?apikey={token_accu}&language=ru&details=true&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    date=json_data['DailyForecasts'][day]['Date']#дата
    temperaturemin=json_data['DailyForecasts'][day]['Temperature']['Minimum']['Value'] #температура min
    temperaturemax=json_data['DailyForecasts'][day]['Temperature']['Maximum']['Value']
    feeltemperaturemin= json_data['DailyForecasts'][day]['RealFeelTemperature']['Minimum']['Value']
    feeltemperaturemax= json_data['DailyForecasts'][day]['RealFeelTemperature']['Minimum']['Value']#ощущаемая температура
    precipitation=json_data['DailyForecasts'][day]['Day']['PrecipitationProbability'] #осадки вероятность
    windspeed=json_data['DailyForecasts'][day]['Day']['Wind']['Speed']['Value'] #скорость ветра в км/ч
    winddir=json_data['DailyForecasts'][day]['Day']['Wind']['Direction']['Localized']# направление ветра
    phrase=json_data['DailyForecasts'][day]['Day']['IconPhrase']#фраза о погоде, облачно и тп.
    return date, temperaturemin,temperaturemax ,feeltemperaturemin,feeltemperaturemax, precipitation, windspeed, winddir, phrase


def job(chatid : str, city : str):    #функция отправки уведомления
    if chatid is not None:
        print ("Отправлено") 
        ct=city
        latitude, longitude=geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        date, temperaturemin,temperaturemax ,feeltemperaturemin,feeltemperaturemax, precipitation, windspeed, winddir, phrase = weather_day(cod_loc, token_accu)
        temperature=(temperaturemax+temperaturemin)/2
        feeltemperature=(temperaturemax+temperaturemin)/2
        bot.send_message(chatid,f"Уведомление: В городе {ct} {phrase}, средняя температура {temperature}°C, ветер {winddir}"+" "+f"{windspeed} км/ч")
        if feeltemperature <= -20:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет очень холодно и метель!🌬❄️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет очень холодно и идет снег!❄️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет очень холодно!☃️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет очень холодно!☃️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤 и шерстяные носки🧦")
        if feeltemperature > -20 and feeltemperature <= -10:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно и метель!🌬❄️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно и  снег!❄️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно!☃️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно!☃️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦")
        if feeltemperature > -10 and feeltemperature <= 0:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно и метель! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно и  снег! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня на улице будет холодно! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤")
        if feeltemperature > 0 and feeltemperature <= 10:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня будет дождь и сильный ветер!🌧🌬Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять дождевик!")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня будет дождь!🌧 Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять зонтик!☔️")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня на улице будет сильный ветер!🌬 Предлагаем вам надеть пальто🥋, ботинки👞 и не забудьте шарф🧣")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня без осадков!🌬 Предлагаем вам надеть пальто🥋 и ботинки👞")
        if feeltemperature > 10 and feeltemperature <= 15:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня будет очень ветрено и  дождь!🌬🌧 Предлагаем вам надеть свитер🦺 и джинсы👖, а также не забудьте взять дождевик!")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня будет дождь!🌧 Предлагаем вам надеть водолазку и джинсы👖, а также не забудьте взять зонтик!☔️")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня будет очень ветрено!🌬 Предлагаем вам надеть свитер🦺 и джинсы👖")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня будет хорошая погода!🤗Предлагаем вам надеть водолазку и джинсы👖")
        if feeltemperature > 15:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня будет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять дождевик!☔️")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня  тепло, но будет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять зонтик!☔️")
            else:
                if windspeed >= 36:
                    bot.send_message(chatid,f"Сегодня будет жаркая погода! 🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒")
                if windspeed < 36:
                    bot.send_message(chatid,f"Сегодня будет отличная погода!🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒")
                    
while True:  #бесконечный цикл проверки времени, что бы отправлять уведомления
    df=pd.read_excel('./ntfDB.xlsx') # обновление датафрейма, если былы изменена информация
    schedule.run_pending()
    schedule.clear() # очистка созданных расписаний
    for i in range(len(df)):
        schedule.every().day.at(str(df['ntftime'][i])).do(job, df['id'][i], df['city'][i]) #создание расписание под каждую строку таблицы эксель
    print(schedule.jobs)  #печатает в питоне существующие расписания и их информацию
    schedule.run_pending()
    time.sleep(10) # ждет 10 секунд


# In[ ]:





# In[ ]:




