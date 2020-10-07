#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from urllib.parse import urlencode, unquote
import requests
import time
from datetime import datetime
import bot_settings as bs
import telepot
from  natsort import natsorted


# In[3]:




def get_file_name(url):
    file_name = url.split('&')[1][9:]
    return file_name


def download_file(public_key):

    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    with open(os.path.join('data', unquote(get_file_name(download_url))), 'wb') as f:
        print('Загрузка файла', unquote(get_file_name(download_url)))
        f.write(download_response.content)

def calc_days_from_start(start_day):
    """Подсчет количества дней с начала марафона"""
    days_from_start = datetime.now().date() - datetime.strptime(start_day, '%d.%m.%Y').date()
    return days_from_start.days  
        
def send_message_to_tlg(file):
    """Отправка сообщений в телеграмм"""
#     requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
#        chat_id=bs.ID_chat,
#        text=message))
    with open(os.path.join('data', file), 'r') as txt:
        bot.sendMessage(bs.ID_chat, txt.read())
    
def send_video_to_tlg(file):
    """Отправка видео в телеграмм"""
#     requests.get('https://api.telegram.org/bot{}/sendVideo'.format(bs.token), params=dict(
#        chat_id=bs.ID_chat,
#        video=video))    
    with open(os.path.join('data', file), 'rb') as mov:
        bot.sendVideo(bs.ID_chat, mov, width=20, height=11)
        
        
def send_doc_to_tlg(file):
    """Отправка фалов в телеграмм"""
#     requests.get('https://api.telegram.org/bot{}/sendDocument'.format(bs.token), params=dict(
#        chat_id=bs.ID_chat,
#        document=document))
    with open(os.path.join('data', file), 'rb') as doc:
        bot.sendDocument(bs.ID_chat, doc)

def send_data_to_tlg(file_name):
    file_extension = file_name.split('.')[1] # расширение файла
    if file_extension == 'txt':
        send_message_to_tlg(file_name)
        print(datetime.today().time(), 'send text', file_name)
    elif file_extension == 'mov':
        send_video_to_tlg(file_name)
        print(datetime.today().time(), 'send video', file_name)
    else:
        send_doc_to_tlg(file_name)
        print(datetime.today().time(), 'send doc', file_name)


# In[ ]:


# Загрузка файлов с диска

for day_links in bs.links:
    for link in day_links:
        download_file(link)
print('\nВсе файл загружены')


# In[ ]:


# Подготовка списка файлов
files_list = os.listdir('data')
files_list = natsorted(files_list)
files_list


# In[ ]:


# Создание экземпляра бота
bot = telepot.Bot(bs.token)

# Отправка стартовых сообщений - день 0

for file_name in files_list:
    file_extension = file_name.split('.')[1] # расширение файла
    if ('day_0' in file_name) and (datetime.today().date() <= datetime.strptime(bs.start_day, '%d.%m.%Y').date()) and (time.localtime().tm_hour < bs.send_hour):
        send_data_to_tlg(file_name)

print('Сообщения отправлены')


# In[ ]:


# Проверка данных

total_days = datetime.strptime(bs.finish_day, '%d.%m.%Y').date() - datetime.strptime(bs.start_day, '%d.%m.%Y').date()
print('Общая продолжительность марафона - {} дней'.format(total_days.days + 1))


if total_days.days + 3 != len(bs.links):
    print('Количество дней марафона не равно количеству дней в конфигурационном файле!')
else:
    print('Данные в порядке!')


# In[ ]:


# prev_day = time.localtime().tm_min # раскомменитровать для тестирования
prev_day = time.localtime().tm_mday # закомментировать для тестирования

# prev_hour = time.localtime().tm_sec # раскомменитровать для тестирования
prev_hour = time.localtime().tm_hour # закомментировать для тестирования

# days_from_start = 0 # раскомменитровать для тестирования   

flag = True # флаг отправки сообщения в первый день
readiness = True


# In[ ]:



while total_days.days + 3 == len(bs.links):
    
    # отправка сообщения владельцу, что бот запущен
    if readiness:
        print(datetime.today().time(), 'Бот запущен.')
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
            chat_id=bs.owner_id,
            text='Бот запущен.'))
        readiness = False
    
    
    # Триггер по дням
#     day = time.localtime().tm_min # раскомменитровать для тестирования
    day = time.localtime().tm_mday # закомментировать для тестирования
    if day != prev_day:
        prev_day = day
        days_from_start = calc_days_from_start(bs.start_day) # закомментировать для тестирования
        
        print(datetime.today().time(), 'Прошло {} дней с начала марафона'.format(days_from_start))
        
    # Триггер по часам
#     hour = time.localtime().tm_sec # раскомменитровать для тестирования
    hour = time.localtime().tm_hour # закомментировать для тестирования
    if hour != prev_hour:
        prev_hour = hour

        # Отправка сообщения о готовности бота отправлять сообщения в чат
        if hour == bs.readiness_hour:
            print(datetime.today().time(), 'Бот готов отправлять сообщения в чат.')
            requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
                chat_id=bs.owner_id,
                text='Бот готов отправлять сообщения в чат.'))  
    
        # Отправка первого сообщения в чат - за час до основных
#         if hour == bs.send_hour - 10: # раскомменитровать для тестирования
        if hour == bs.send_hour - 1: # закомментировать для тестирования
            for file_name in files_list:
                if ('day_0' not in file_name) and ('day_1_msg_1' not in file_name) and ('msg_1.txt' in file_name) and ('day_{}'.format(days_from_start+1) in file_name):
                    send_data_to_tlg('day_{}_msg_1.txt'.format(days_from_start+1))
            

        # Отправка сообщения в чат
        if hour == bs.send_hour:
            for file_name in files_list:
                if (days_from_start > total_days.days) and ('day_П' in file_name):
                    send_data_to_tlg(file_name)
                    print(datetime.today().time(), 'Congrats! Marathon is over.')
                elif ('day_0' not in file_name) and ('msg_1.txt' not in file_name) and ('day_{}'.format(days_from_start+1) in file_name):
                    send_data_to_tlg(file_name)
#                 elif ('day_1_msg_1' in file_name) and flag: # раскомменитровать для тестирования
                elif ('day_1_msg_1' in file_name) and (datetime.today().date() == datetime.strptime(bs.start_day, '%d.%m.%Y').date()) and flag: # закомменитровать для тестирования
                    
                    send_data_to_tlg(file_name)
                    flag = False
            
#             days_from_start += 1 # раскомменитровать для тестирования
            
            if days_from_start >= total_days.days + 2:
                break


# # Для получения ID чата нужно в адресную строку браузера скопировать ссылку (чат при этом должен быть публичным):
# 
# https://api.telegram.org/bot1318094188:AAEpy6lDo4Ld5FwPyvY6vQGDsncVKGvo148/sendMessage?chat_id=@nvofmyself&text=123
#         
# # После можно сделать чат приватным     
# 
# {"ok":true,"result":{"message_id":2,"chat":{"id":-1001205176666,"title":"\u041c\u0430\u0440\u0430\u0444\u043e\u043d \"\u041d\u043e\u0432\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f \u0441\u0435\u0431\u044f-2\"","username":"nvofmyself","type":"channel"},"date":1601981448,"text":"123"}}

# In[ ]:




