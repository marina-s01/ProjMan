#!/usr/bin/env python
# coding: utf-8

# In[7]:


import telebot; #библиотека для работы с телеграм-ботами
import json
import requests as req
from telebot import types
from geopy import geocoders
from geopy.geocoders import Nominatim
from datetime import timedelta, datetime
import requests
from datetime import timedelta, datetime, time
import pandas as pd
import numpy as np
bot = telebot.TeleBot('5688775484:AAFfcMbAm_t-qEOnuqanR63ivL4UJ-qJdeY') #переменная для работы с ботом через токен\
token_accu="o8bQ6kOLDIm242Z9wZqvderTlzk6ynVR" #  токены: GuL1TlbAFOb3BDTnqE88YwIWmHXyhXCn    7pNet2S89J6HC7m6DdPIh5beY93ZhPOS    o8bQ6kOLDIm242Z9wZqvderTlzk6ynVR

day1 = datetime.now()+timedelta(1)
day2 = datetime.now()+timedelta(2)
day3 = datetime.now()+timedelta(3)
day4 = datetime.now()+timedelta(4)

#Меню Узнать погоду, Настройки, Обратная связь
def menu1():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Узнать погоду")
    button2 = types.KeyboardButton("Настройки")
    button3 = types.KeyboardButton("Обратная связь")
    murkup.add(button1, button2, button3)
    return murkup

#Меню Выбрать город, определить геолокацию
def menu2():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button4 = types.KeyboardButton("Выбрать город")
    button5 = types.KeyboardButton("Определить геолокацию", request_location=True)
    button6 = types.KeyboardButton("Главное меню")
    murkup.add(button4, button5, button6)
    return murkup

#Меню Узнать погоду сейчас и по времени
def menu3():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button7 = types.KeyboardButton("Узнать погоду сейчас")
    button8 = types.KeyboardButton("Узнать погоду по времени")
    button9 = types.KeyboardButton("Главное меню")
    murkup.add(button7)#, button8, button9)
    murkup.add(button8)
    murkup.add(button9)
    return murkup

#Меню Изменить город и Уведомления
def menu4():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button9 = types.KeyboardButton("Изменить город")
    button17 = types.KeyboardButton("Уведомления")
    button10 = types.KeyboardButton("Главное меню")
    murkup.add(button9, button17, button10)
    return murkup

#Меню Получить рекомендации
def menu5():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button11 = types.KeyboardButton("Получить рекомендации одежды")
    button12 = types.KeyboardButton("Главное меню")
    murkup.add(button11, button12)
    return murkup

#Меню Выбор дня
def menu6():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button13 = types.KeyboardButton(day1.strftime("%d-%m-%Y"))
    button14 = types.KeyboardButton(day2.strftime("%d-%m-%Y"))
    button15 = types.KeyboardButton(day3.strftime("%d-%m-%Y"))
    button16 = types.KeyboardButton(day4.strftime("%d-%m-%Y"))
    murkup.add(button13, button14, button15, button16)
    return murkup

#Меню Изменить город и Уведомления
def menu7():
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button18 = types.KeyboardButton("Выбрать время")
    button19 = types.KeyboardButton("Отключить уведомления")
    murkup.add(button18, button19)
    return murkup


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

def weather_now(cod_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{cod_loc}?apikey={token_accu}&language=ru&details=true&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    temperature=json_data[0]['Temperature']['Value'] #температура
    feeltemperature= json_data[0]['RealFeelTemperature']['Value'] #ощущаемая температура
    precipitation=json_data[0]['HasPrecipitation'] #осадки
    windspeed=json_data[0]['Wind']['Speed']['Value'] #скорость ветра в км/ч
    winddir=json_data[0]['Wind']['Direction']['Localized']# направление ветра
    phrase=json_data[0]['IconPhrase']#фраза о погоде, облачно и тп.
    humidity=json_data[0]['RelativeHumidity'] #влажность в процентах
    return temperature,feeltemperature, precipitation, windspeed, winddir, phrase, humidity

def weather_day(cod_loc: str, token_accu: str,day: int):
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

#декоратор обработчика сообщений
@bot.message_handler(commands=['start'])
#Начальное приветствие
def send_welcome(message):
    #Кнопки
    bot.reply_to(message, "Здравствуйте! \U0001F44B Добро пожаловать в бот CLOther. \U0001F321")
    bot.reply_to(message, "Здесь вы сможете получать погоду и рекомендации по одежде в нужном вам городе.")
    bot.reply_to(message, "Давайте определим город, погода которого вас интересует, для этого воспользуйтесь кнопками ниже \U0001F447", reply_markup=menu2())


city = ""
cities = [
  "Бердск", "Барабинск", "Искитим",
  "Карасук", "Новосибирск", "Обь",
  "Татарск", "Черепаново", "Тогучин"]

Lat = ""
Long = ""

#Определение геолокации
@bot.message_handler(content_types=['location'])
def handle_loc(message):
    global Long, Lat, city
    geolocator = Nominatim(user_agent="geoapiExercises")
    if message.location is not None:
        bot.send_message == (message.location)
        geolocator = Nominatim(user_agent="geoapiExercises")
        Lat = message.location.latitude
        Long = message.location.longitude
        location = geolocator.reverse(str(Lat)+","+str(Long))
        address = location.raw['address']
        city = str(address.get('city'))
        bot.send_message(message.chat.id, "Отлично! Ваш город - " + city, reply_markup=menu1())
    bot.register_next_step_handler(message, menu_weather)


#Работа с кнопками
@bot.message_handler(content_types=['text'])
def menu_one(message):
    if message.text == "Выбрать город":
        bot.send_message(message.from_user.id, 'Введите название города…Например, Новосибирск.')
        bot.register_next_step_handler(message, get_city)
    elif message.text == "Определить геолокацию":
        bot.register_next_step_handler(message, handle_loc)
    #   global city
    #   city="Новосибирск"
    #   bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
    #   bot.register_next_step_handler(message, menu_weather)
    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)


@bot.message_handler(content_types=['text'])
def get_city(message): #получаем город
    global city
    city = message.text
    if city in cities:
        bot.send_message(message.chat.id, 'Город успешно изменен! Теперь вы будете получать погоду и рекомендации по одежде для города ' + str(city), reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)
    else:
        bot.send_message(message.from_user.id, 'Данного города нет в списке, попробуйте еще раз!')
        bot.register_next_step_handler(message, get_city)

#Основное меню
@bot.message_handler(content_types=['text'])
def menu_weather(message):
    if message.text == "Узнать погоду":
        bot.send_message(message.chat.id, "Какая погода вас интересует? В данный момент или определенный?", reply_markup=menu3())
        bot.register_next_step_handler(message, send_weather)
    elif message.text == "Настройки":
        bot.send_message(message.chat.id, "Укажите, погода которого вас интересует, для этого воспользуйтесь кнопками ниже", reply_markup=menu4())
        bot.register_next_step_handler(message, edit_city)
    elif message.text == "Обратная связь":
        bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)

#Проверка записи времени
@bot.message_handler(content_types=['text'])
def check(d):
    ntftime = d
    try:
        datetime.strptime(ntftime, '%H:%M')
        return ntftime
    except:
          return False

#Добавление записи об уведомлении в эксель
#учет пользоваетеля в списке, внесение изменений в его данные
#предусмотрено добавление нового пользователя
@bot.message_handler(content_types=['text'])
def check_time(message):
    ntftime = message.text
    user_id = message.from_user.id
    final_time = check(ntftime)
    if final_time == False:
        bot.send_message(message.from_user.id, 'Время уведомлений набрано неверно! Попробуйте еще раз')
        bot.register_next_step_handler(message, check_time)
    else:
        df=pd.read_excel('./ntfDB.xlsx', index_col=0)
        if any(df['id'] == user_id):
            idx = df.index[df['id'] == user_id]
            df['city'][idx] = city
            df['ntftime'][idx] = ntftime
            df.to_excel('./ntfDB.xlsx')
        else:
            new_row = {'id':user_id, 'ntftime':ntftime, 'city':city}
            df = df.append(new_row, ignore_index=True)
            df.to_excel('./ntfDB.xlsx', index=False)
        bot.send_message(message.chat.id, 'Время уведомлений успешно выбрано!', reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)

@bot.message_handler(content_types=['text'])
def menu_notif(message):
    chat_id = message.chat.id
    if message.text == "Выбрать время":
        bot.send_message(message.from_user.id, 'Пожалуйста, введите время получения уведомлений согласно маске ##:##')
        bot.register_next_step_handler(message, check_time)
    elif message.text == "Отключить уведомления":
        df=pd.read_excel('./ntfDB.xlsx', index_col=0)
        #print(df)
        df = df.drop(np.where(df['id'] == chat_id)[0])
        df.to_excel('./test.xlsx', index=False)
        #print(df)
        df2=pd.read_excel('./test.xlsx', index_col=0)
        df2=pd.read_excel('./test.xlsx', index_col=0)
        df2.to_excel('./ntfDB.xlsx', index=False)
        bot.send_message(message.chat.id, "Уведомления отключены!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)
    elif message.text == "Главное меню":
       bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
       bot.register_next_step_handler(message, menu_weather)


@bot.message_handler(content_types=['text'])
def edit_city(message):
    if message.text == "Изменить город":
       bot.send_message(message.chat.id, "Давайте определим город, погода которого вас интересует, для этого воспользуйтесь кнопками ниже", reply_markup=menu2())
       bot.register_next_step_handler(message, menu_one)
    elif message.text == "Уведомления":
       bot.send_message(message.chat.id, "Отлично!", reply_markup=menu7())
       bot.register_next_step_handler(message, menu_notif)
    elif message.text == "Главное меню":
       bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
       bot.register_next_step_handler(message, menu_weather)

@bot.message_handler(content_types=['text'])
def send_weather(message):
    if message.text == "Узнать погоду сейчас":
        latitude, longitude = geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        temperature, feeltemperature, precipitation, windspeed, winddir, phrase, humidity = weather_now(cod_loc, token_accu)
        bot.send_message(message.chat.id,f"Сейчас в городе {city} {phrase}, {temperature}°C , ветер {winddir}"+" "+f"{windspeed} км/ч",reply_markup=menu5())
        bot.register_next_step_handler(message, rec)

    elif message.text == "Узнать погоду по времени":
       #выбор дня, не позднее 5 дней с сегодняшнего дня, и поиск разницы с сегодняшней датой
        bot.send_message(message.chat.id, "Выберите день", reply_markup=menu6())
        bot.register_next_step_handler(message, menu_day)
    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)


@bot.message_handler(content_types=['text'])     #выбор дня, не позднее 5 дней с сегодняшнего дня, и поиск разницы с сегодняшней датой
def menu_day(message):
    global day_rec
    if message.text == day1.strftime("%d-%m-%Y"):
        #murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=1
        day_rec = 1
        #bot.send_message(message.chat.id, "Отлично!", reply_markup=menu6())
        weather_choose(message, day,city,token_accu)
    elif message.text == day2.strftime("%d-%m-%Y"):
        #murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=2
        day_rec = 2
        #bot.send_message(message.chat.id, "Отлично!", reply_markup=menu6())
        weather_choose(message, day,city,token_accu)
    elif message.text == day3.strftime("%d-%m-%Y"):
        #murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=3
        day_rec = 3
        #bot.send_message(message.chat.id, "Отлично! ", reply_markup=menu6())
        weather_choose(message, day,city,token_accu)
    elif message.text == day4.strftime("%d-%m-%Y"):
        #murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=4
        day_rec = 4
        #bot.send_message(message.chat.id, "Отлично!  ", reply_markup=menu6())
        weather_choose(message, day,city,token_accu)
    else: bot.send_message(message.from_user.id, 'Упс! Ошибочка!')

@bot.message_handler(content_types=['text'])
def weather_choose(message, day: int,city: str,token_accu: str):
        latitude, longitude=geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        date, temperaturemin,temperaturemax ,feeltemperaturemin,feeltemperaturemax, precipitation, windspeed, winddir, phrase = weather_day(cod_loc, token_accu,day)
        temperature= (temperaturemax+temperaturemin)/2
        bot.send_message(message.chat.id,f"В городе {city} {phrase}, средняя температура {temperature}°C , ветер {winddir}"+" "+f"{windspeed} км/ч",reply_markup=menu5())
        bot.register_next_step_handler(message, rec2)

@bot.message_handler(content_types=['text']) #вывод рекомендаций по одежде после нажатия кнопки "погода сейчас"
def rec(message):
    if message.text == "Получить рекомендации одежды":
        latitude, longitude = geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        temperature, feeltemperature, precipitation, windspeed, winddir, phrase, humidity = weather_now(cod_loc, token_accu)

        if feeltemperature <= -20:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице очень холодно и метель!🌬❄️ Надень термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице очень холодно и идет снег!❄️ Надень термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице очень холодно!☃️ Надень термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице очень холодно!☃️ Надень термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
        if feeltemperature > -20 and feeltemperature <= -10:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице  холодно и метель!🌬❄️ Надень пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице  холодно и идет снег!❄️ Надень пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице  холодно!☃️ Надень пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице  холодно!☃️ Надень пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
        if feeltemperature > -10 and feeltemperature <= 0:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице холодно и метель! ⛄️ Надень теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице холодно и идет снег! ⛄️ Надень теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице холодно! ⛄️ Надень теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице холодно! ⛄️ Надень теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤",reply_markup=menu5())
        if feeltemperature > 0 and feeltemperature <= 10:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас идет дождь и сильный ветер!🌧🌬Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять дождевик!",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас идет дождь!🌧 Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас на улице сильный ветер!🌬 Предлагаем вам надеть пальто🥋, ботинки👞 и не забудьте шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас на улице без осадков!🌬 Предлагаем вам надеть пальто🥋 и ботинки👞",reply_markup=menu5())
        if feeltemperature > 10 and feeltemperature <= 15:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас очень ветрено и идет дождь!🌬🌧 Предлагаем вам надеть свитер🦺 и джинсы👖, а также не забудьте взять дождевик!",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас идет дождь!🌧 Предлагаем вам надеть водолазку и джинсы👖, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас очень ветрено!🌬 Предлагаем вам надеть свитер🦺 и джинсы👖",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас хорошая погода!🤗Предлагаем вам надеть водолазку и джинсы👖",reply_markup=menu5())
        if feeltemperature > 15:
            if precipitation == True:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Идет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять дождевик!☔️",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас тепло, но идет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,"Сейчас жаркая погода! 🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,"Сейчас отличная погода!🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒",reply_markup=menu5())

    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)

@bot.message_handler(content_types=['text']) #вывод рекомендаций по одежде после нажатия кнопки "погода по времени"
def rec2(message):
    if message.text == "Получить рекомендации одежды":
        latitude, longitude=geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        date, temperaturemin,temperaturemax ,feeltemperaturemin,feeltemperaturemax, precipitation, windspeed, winddir, phrase = weather_day(cod_loc, token_accu,day_rec)
        feeltemperature = (feeltemperaturemax+feeltemperaturemin)/2
        date = date[:10]

        if feeltemperature <= -20:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет очень холодно и метель!🌬❄️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет очень холодно и идет снег!❄️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет очень холодно!☃️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет очень холодно!☃️ Наденьте термобелье, пуховик🧥, головной убор🎩, закрывающий уши , теплые ботинки👢, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
        if feeltemperature > -20 and feeltemperature <= -10:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно и метель!🌬❄️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно и  снег!❄️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно!☃️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤, шарф🧣 и шерстяные носки🧦",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно!☃️ Наденьте пуховик🧥, головной убор🎩, теплые ботинки🥾, варежки🧤 и шерстяные носки🧦",reply_markup=menu5())
        if feeltemperature > -10 and feeltemperature <= 0:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно и метель! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно и  снег! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 , перчатки🧤  и шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет холодно! ⛄️ Наденьте теплую куртку🥼, шапку🎩, теплые ботинки👞 и  перчатки🧤",reply_markup=menu5())
        if feeltemperature > 0 and feeltemperature <= 10:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} будет дождь и сильный ветер!🌧🌬Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять дождевик!",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} будет дождь!🌧 Предлагаем вам надеть куртку🥋 и ботинки👞, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} на улице будет сильный ветер!🌬 Предлагаем вам надеть пальто🥋, ботинки👞 и не забудьте шарф🧣",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} без осадков!🌬 Предлагаем вам надеть пальто🥋 и ботинки👞",reply_markup=menu5())
        if feeltemperature > 10 and feeltemperature <= 15:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} будет очень ветрено и  дождь!🌬🌧 Предлагаем вам надеть свитер🦺 и джинсы👖, а также не забудьте взять дождевик!",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} будет дождь!🌧 Предлагаем вам надеть водолазку и джинсы👖, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} будет очень ветрено!🌬 Предлагаем вам надеть свитер🦺 и джинсы👖",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} будет хорошая погода!🤗Предлагаем вам надеть водолазку и джинсы👖",reply_markup=menu5())
        if feeltemperature > 15:
            if precipitation > 60:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} будет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять дождевик!☔️",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date}  тепло, но будет дождь!🌧 Предлагаем вам надеть футболку👕 и джинсы👖, а также не забудьте взять зонтик!☔️",reply_markup=menu5())
            else:
                if windspeed >= 36:
                    bot.send_message(message.chat.id,f"{date} будет жаркая погода! 🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒",reply_markup=menu5())
                if windspeed < 36:
                    bot.send_message(message.chat.id,f"{date} будет отличная погода!🙃Предлагаем вам надеть футболку👕 и шорты🩳, а также не забудьте очки🕶 и кепку🧢 или шляпу👒",reply_markup=menu5())
        #bot.register_next_step_handler(message, menu_weather)

    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, "Отлично!", reply_markup=menu1())
        bot.register_next_step_handler(message, menu_weather)

bot.polling(none_stop=True, interval=0) #бесконечный запрос у сервера телеграмма
