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
bot = telebot.TeleBot('5688775484:AAFfcMbAm_t-qEOnuqanR63ivL4UJ-qJdeY') #переменная для работы с ботом через токен\
token_accu="7pNet2S89J6HC7m6DdPIh5beY93ZhPOS" #  токены: GuL1TlbAFOb3BDTnqE88YwIWmHXyhXCn    7pNet2S89J6HC7m6DdPIh5beY93ZhPOS    o8bQ6kOLDIm242Z9wZqvderTlzk6ynVR

day1 = datetime.now()+timedelta(1)
day2 = datetime.now()+timedelta(2)
day3 = datetime.now()+timedelta(3)
day4 = datetime.now()+timedelta(4)


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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Выбрать город")
    button2 = types.KeyboardButton("Определить геолокацию", request_location=True)
    markup.add(button1, button2)	
    bot.reply_to(message, "Здравствуйте! \U0001F44B Добро пожаловать в бот CLOther. \U0001F321")
    bot.reply_to(message, "Здесь вы сможете получать погоду и рекомендации по одежде в нужном вам городе.")
    bot.reply_to(message, "Давайте определим город, погода которого вас интересует, для этого воспользуйтесь кнопками ниже", reply_markup=markup)

city = ""
cities = [
  "Бердск", "Барабинск", "Искитим",
  "Карасук", "Новосибирск", "Обь",
  "Татарск", "Черепаново", "Тогучин"]

Lat = ""
Long = ""

@bot.message_handler(content_types=['location'])
def handle_loc(message):
    global Long, Lat, city
    geolocator = Nominatim(user_agent="geoapiExercises")
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button10 = types.KeyboardButton("Узнать погоду")
    button11 = types.KeyboardButton("Настройки")
    button12 = types.KeyboardButton("Обратная связь")
    murkup.add(button10, button11, button12)
    if message.location is not None:
        bot.send_message == (message.location)
        geolocator = Nominatim(user_agent="geoapiExercises")
        Lat = message.location.latitude
        Long = message.location.longitude
        location = geolocator.reverse(str(Lat)+","+str(Long))
        address = location.raw['address']
        city = str(address.get('city'))
        bot.send_message(message.chat.id, "Отлично! Ваш город - " + city, reply_markup=murkup)
    bot.register_next_step_handler(message, menu_weather)
    
#Коды: новосибирск-294459
    
#Работа с кнопками
@bot.message_handler(content_types=['text'])
def menu_one(message):
    if message.text == "Выбрать город":
        bot.send_message(message.from_user.id, 'Введите название города…Например, Новосибирск.')
        bot.register_next_step_handler(message, get_city)
    elif message.text == "Определить геолокацию":
        bot.register_next_step_handler(message, handle_loc)

@bot.message_handler(content_types=['text'])
def get_city(message): #получаем город
    global city
    city = message.text	
    if city in cities:
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button4 = types.KeyboardButton("Узнать погоду")
        button5 = types.KeyboardButton("Настройки")
        button6 = types.KeyboardButton("Обратная связь")
        murkup.add(button4, button5, button6)
        bot.send_message(message.chat.id, 'Город успешно изменен! Теперь вы будете получать погоду и рекомендации по одежде для города ' + str(city), reply_markup=murkup)
        bot.register_next_step_handler(message, menu_weather)
    else:
        bot.send_message(message.from_user.id, 'Данного города нет в списке, попробуйте еще раз!')
        bot.register_next_step_handler(message, get_city)
    
#Основное меню
@bot.message_handler(content_types=['text'])
def menu_weather(message):
    if message.text == "Узнать погоду":
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button7 = types.KeyboardButton("Узнать погоду сейчас")
        button8 = types.KeyboardButton("Узнать погоду по времени")
        murkup.add(button7, button8)
        bot.send_message(message.chat.id, "Какая погода вас интересует? В данный момент или определенный?", reply_markup=murkup)
        bot.register_next_step_handler(message, send_weather)
    elif message.text == "Настройки":
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button9 = types.KeyboardButton("Изменить город")
        murkup.add(button9)
        bot.send_message(message.chat.id, "Укажите, погода которого вас интересует, для этого воспользуйтесь кнопками ниже", reply_markup=murkup)
    elif message.text == "Обратная связь":
        bot.send_message(message.chat.id, "Отлично!") 
        
        
@bot.message_handler(content_types=['text'])        
def send_weather(message):
    if message.text == "Узнать погоду сейчас":
        latitude, longitude = geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        temperature, feeltemperature, precipitation, windspeed, winddir, phrase, humidity = weather_now(cod_loc, token_accu)
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button13 = types.KeyboardButton("Узнать погоду")
        button14 = types.KeyboardButton("Настройки")
        button15 = types.KeyboardButton("Обратная связь")
        murkup.add(button13, button14, button15)
        bot.send_message(message.chat.id,f"Сейчас в городе {city} {phrase}, {temperature}°C , ветер {winddir}"+" "+f"{windspeed} км/ч",reply_markup=murkup)
        bot.register_next_step_handler(message, menu_weather)
    elif message.text == "Узнать погоду по времени":
       #выбор дня, не позднее 5 дней с сегодняшнего дня, и поиск разницы с сегодняшней датой
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button19 = types.KeyboardButton(day1.strftime("%d-%m-%Y"))
        button20 = types.KeyboardButton(day2.strftime("%d-%m-%Y"))
        button21 = types.KeyboardButton(day3.strftime("%d-%m-%Y"))
        button22 = types.KeyboardButton(day4.strftime("%d-%m-%Y"))
        murkup.add(button19, button20, button21, button22)
        bot.send_message(message.chat.id, "Выберите день", reply_markup=murkup)
        bot.register_next_step_handler(message, menu_day)

@bot.message_handler(content_types=['text'])     #выбор дня, не позднее 5 дней с сегодняшнего дня, и поиск разницы с сегодняшней датой    
def menu_day(message):
    if message.text == day1.strftime("%d-%m-%Y"):
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=1
        bot.send_message(message.chat.id, "Отлично!", reply_markup=murkup)
        weather_choose(message, day,city,token_accu)
    elif message.text == day2.strftime("%d-%m-%Y"):
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=2
        bot.send_message(message.chat.id, "Отлично!", reply_markup=murkup)
        weather_choose(message, day,city,token_accu)
    elif message.text == day3.strftime("%d-%m-%Y"):
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=3
        bot.send_message(message.chat.id, "Отлично! ", reply_markup=murkup)
        weather_choose(message, day,city,token_accu)
    elif message.text == day4.strftime("%d-%m-%Y"):
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        day=4
        bot.send_message(message.chat.id, "Отлично!  ", reply_markup=murkup)
        weather_choose(message, day,city,token_accu)
    else: bot.send_message(message.from_user.id, 'Упс! Ошибочка!')
    
@bot.message_handler(content_types=['text'])
def weather_choose(message, day: int,city: str,token_accu: str):         
        latitude, longitude=geo_pos(city)
        cod_loc = code_location(latitude, longitude, token_accu)
        date, temperaturemin,temperaturemax ,feeltemperaturemin,feeltemperaturemax, precipitation, windspeed, winddir, phrase = weather_day(cod_loc, token_accu,day)
        temperature= (temperaturemax+temperaturemin)/2
        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button16 = types.KeyboardButton("Узнать погоду")
        button17 = types.KeyboardButton("Настройки")
        button18 = types.KeyboardButton("Обратная связь")
        murkup.add(button16, button17, button18)
        bot.send_message(message.chat.id,f"В городе {city} {phrase}, средняя температура {temperature}°C , ветер {winddir}"+" "+f"{windspeed} км/ч",reply_markup=murkup)
        bot.register_next_step_handler(message, menu_weather)
    
    
bot.polling(none_stop=True, interval=0) #бесконечный запрос у сервера телеграмма


# In[ ]: