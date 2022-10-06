#!/usr/bin/env python
# coding: utf-8

# In[8]:


import telebot; #библиотека для работы с телеграм-ботами
bot = telebot.TeleBot('5688775484:AAFfcMbAm_t-qEOnuqanR63ivL4UJ-qJdeY'); #переменная для работы с ботом через токен\

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
      bot.send_message(message.from_user.id, "Здесь должен быть текст для помощи по командом бота.")
    
    
bot.polling(none_stop=True, interval=0) #бесконечный запрос у сервера телеграмма

