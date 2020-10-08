#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from urllib.parse import urlencode, unquote
import requests
import time
from datetime import datetime
import bot_settings as bs
import telepot


# In[ ]:


def get_file_name(url):
    file_name = url.split('&')[1][9:]
    return file_name


def download_file(public_key):
    """Загрузка файла и возврат имени загруженного файла"""
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    with open(os.path.join('data', unquote(get_file_name(download_url))), 'wb') as f:
        file_name = unquote(get_file_name(download_url))
        f.write(download_response.content)
        print('{}: загружен файла {}'.format(datetime.today(), file_name))
    
    return file_name


def calc_days_from_start(start_day=bs.start_day):
    """Подсчет количества дней с начала марафона"""
    days_from_start = datetime.now().date() - datetime.strptime(start_day, '%d.%m.%Y').date()
    days_from_start = days_from_start.days
    print('{}: день марафона: {}'.format(datetime.today(), days_from_start + 1))
    return days_from_start


def send_message_to_tlg(file):
    """Отправка сообщений в телеграмм"""
    with open(os.path.join('data', file), 'r') as txt:
        bot.sendMessage(bs.chat_id, txt.read())

        
def send_video_to_tlg(file):
    """Отправка видео в телеграмм"""
    with open(os.path.join('data', file), 'rb') as mov:
        bot.sendVideo(bs.chat_id, mov, width=20, height=11)
        
        
def send_doc_to_tlg(file):
    """Отправка фалов в телеграмм"""
    with open(os.path.join('data', file), 'rb') as doc:
        bot.sendDocument(bs.chat_id, doc)

        
def send_data_to_tlg(file_name):
    file_extension = file_name.split('.')[1] # расширение файла
    if file_extension == 'txt':
        send_message_to_tlg(file_name)
        print('{}: send text {}'.format(datetime.today(), file_name))
    elif file_extension == 'mov':
        send_video_to_tlg(file_name)
        print('{}: send video {}'.format(datetime.today(), file_name))
    else:
        send_doc_to_tlg(file_name)
        print('{}: send doc {}'.format(datetime.today(), file_name))

        
def check_start_marathon(start_day=bs.start_day, send_hour=bs.send_hour):
    """Проверка начала марафона"""
    marathon_started = (datetime.today().date() >= datetime.strptime(start_day, '%d.%m.%Y').date()) and         (time.localtime().tm_hour >= send_hour)
    return marathon_started


# In[ ]:


# Проверка данных

total_days = datetime.strptime(bs.finish_day, '%d.%m.%Y').date() - datetime.strptime(bs.start_day, '%d.%m.%Y').date()
total_days = total_days.days
print('Общая продолжительность марафона, дней: {}'.format(total_days + 1))


if total_days + 3 != len(bs.links):
    print('Количество дней марафона не равно количеству дней в конфигурационном файле!')
else:
    print('Данные в порядке!')


# In[ ]:


# Создание экземпляра бота
bot = telepot.Bot(bs.token)

# Создание папки data
if not os.path.exists('data'):
    os.makedirs('data')

files_list = [] # Список файлов на отправку

if not check_start_marathon(): # and msgs_not_sent:
    # Загрузка файлов с диска нулевого дня
    print('{}: марафон еще не стартовал, загружаю файлы\n'.format(datetime.today()))
    for link in bs.links[0]:
        print('{}: {}'.format(datetime.today(), link))
        files_list.append(download_file(link))
        
    print('\n{}: файлы нулевого дня загружены'.format(datetime.today()))

    
    # Отправка стартовых сообщений - день 0
    print('\n{}: начинаю отправку сообщений нулевого дня\n'.format(datetime.today()))
    for file_name in files_list:
        send_data_to_tlg(file_name)
    
    print('\n{}: сообщения нулевого дня отправлены'.format(datetime.today()))
else:
    print('\n{}: марафон уже стартовал, сообщения нулевого дня не отправлены!'.format(datetime.today()))

files_list = []


# In[ ]:


prev_day = 99

prev_hour = 99

readiness = False # флаг работы бота (False - бот не работает)

# md = -1 # раскомментировать для тестирования
# h = 0 # раскомментировать для тестирования

while total_days + 3 == len(bs.links):
    
    # уведомление владельца о запуске бота
    if not readiness:
        print('{}: Бот запущен.'.format(datetime.today()))
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
            chat_id=bs.owner_id,
            text='Бот запущен.'))
        readiness = True
    

    hour = time.localtime().tm_hour # закомментировать для тестирования
#     hour = h # раскомментировать для тестирования
    if (hour != prev_hour):
        prev_hour = hour
        
        marathon_day = calc_days_from_start() + 1 # закомментировать для тестирования
#         marathon_day = md # раскомментировать для тестирования
    
        print('marathon_day=', marathon_day, ', hour=', hour, sep='')
    
        if (marathon_day < 1):
            print('\n{}: марафон еще не стартовал'.format(datetime.today()))
    
        else:
            # Загрузка файлов с диска текущего дня за час до отправки
            if hour == bs.send_hour - 2:
                print('{}: загружаю файлы\n'.format(datetime.today()))
                for link in bs.links[marathon_day]:
                    print('{}: {}'.format(datetime.today(), link))
                    files_list.append(download_file(link))

                print('\n{}: файлы загружены'.format(datetime.today()))

                # Отправка сообщения о готовности бота отправлять сообщения в чат
                print(datetime.today().time(), 'Файлы загружены. Бот готов отправлять сообщения в чат.')
                requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
                    chat_id=bs.owner_id,
                    text='Файлы загружены. Бот готов отправлять сообщения в чат.'))  
            
            
            # Отправка сообщений за час до назначенного времени
            if (hour == bs.send_hour - 1) and (marathon_day != 1) and (marathon_day != len(bs.links) - 1):
                print('\n{}: отправляю первое сообщение\n'.format(datetime.today()))
                for file_name in files_list:
                    if 'msg_1.txt' in file_name:
                        send_data_to_tlg(file_name)
                print('\n{}: первое сообщение отправлено\n'.format(datetime.today()))
                del files_list[0]

            # Отправка сообщений в назначенное время
            if hour == bs.send_hour:
                print('\n{}: начинаю отправку сообщений\n'.format(datetime.today()))
                for file_name in files_list:
                    send_data_to_tlg(file_name)
                print('\n{}: сообщения отправлены\n'.format(datetime.today()))
                
                if file_name == 'day_П_msg_1.txt':
                    print('\n{}: Congrats! Marathon is over.'.format(datetime.today()))
                
                files_list = []

            
                
        if marathon_day >= total_days + 3:
            break
            
#         h += 1 # раскомментировать для тестирования
#         if h == 24: # раскомментировать для тестирования
#             h = 0 # раскомментировать для тестирования
#             md += 1  # раскомментировать для тестирования
#             time.sleep(5) # раскомментировать для тестирования

