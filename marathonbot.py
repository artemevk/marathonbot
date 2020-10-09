#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from urllib.parse import urlencode, unquote
import requests
import time
from datetime import datetime
import bot_settings as bs
import telepot


# In[2]:


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
        print('{}: загружен файл {}'.format(datetime.today(), file_name))
    
    return file_name


def calc_days_from_start(start_day=bs.start_day, *m_time):
    """Подсчет количества дней с начала марафона"""
    if m_time:
        structTime = time.localtime(*m_time)
    else:
        structTime = time.localtime()

    days_from_start = datetime(*structTime[:6]).date() - datetime.strptime(start_day, '%d.%m.%Y').date()
    days_from_start = days_from_start.days
    days_from_start
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
        send_message_to_tlg(file_name) # закомментировать для тестирования
        print('{}: send text {}'.format(datetime.today(), file_name))
    elif file_extension == 'mov':
        send_video_to_tlg(file_name) # закомментировать для тестирования
        print('{}: send video {}'.format(datetime.today(), file_name))
    else:
        send_doc_to_tlg(file_name) # закомментировать для тестирования
        print('{}: send doc {}'.format(datetime.today(), file_name))

        
def check_start_marathon(start_day=bs.start_day, send_hour=bs.send_hour, *m_time):
    """Проверка начала марафона"""
    if m_time:
        structTime = time.localtime(*m_time)
    else:
        structTime = time.localtime()
        
    marathon_started = (datetime(*structTime[:6]).date() >= datetime.strptime(start_day, '%d.%m.%Y').date()) and         (time.localtime().tm_hour >= send_hour)
    return marathon_started


# In[3]:


# Задание начальной даты для тестирования

# t = datetime(2020, 10, 8, 0, 0, 0) # раскомментировать для тестирования
# my_time = (t-datetime(1970,1,1)).total_seconds()# раскомментировать для тестирования
# my_time # раскомментировать для тестирования


# In[4]:


# Проверка данных

total_days = datetime.strptime(bs.finish_day, '%d.%m.%Y').date() - datetime.strptime(bs.start_day, '%d.%m.%Y').date()
total_days = total_days.days
print('Общая продолжительность марафона, дней: {}'.format(total_days + 1))


if total_days + 3 != len(bs.links):
    print('Количество дней марафона не равно количеству дней в конфигурационном файле!')
else:
    print('Данные в порядке!')


# In[5]:


# Создание экземпляра бота
bot = telepot.Bot(bs.token)

# Создание папки data
if not os.path.exists('data'):
    os.makedirs('data')

files_list = [] # Список файлов на отправку

if not check_start_marathon(): # закомментировать для тестирования
# if not check_start_marathon(bs.start_day, bs.send_hour, my_time): # раскомментировать для тестирования
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


# In[7]:


prev_day = 99

prev_hour = 99

file_name = ''

readiness = False # флаг работы бота (False - бот не работает)

while total_days + 3 == len(bs.links):
    
    # уведомление владельца о запуске бота
    if not readiness:
        print('{}: Бот запущен.'.format(datetime.today()))
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bs.token), params=dict(
            chat_id=bs.owner_id,
            text='Бот запущен.'))
        readiness = True
    

    hour = time.localtime().tm_hour # закомментировать для тестирования
#     hour = time.localtime(my_time).tm_hour # раскомментировать для тестирования
    if (hour != prev_hour):
        prev_hour = hour
        
#         marathon_day = calc_days_from_start() + 1 # закомментировать для тестирования
        marathon_day = calc_days_from_start(bs.start_day, my_time) + 1  # раскомментировать для тестирования
    
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

        print(files_list)    
                
        if marathon_day >= total_days + 3:
            break
            
            
#     my_time += 0.05 # раскомментировать для тестирования


# 2020-10-09 13:00:00.000541: начинаю отправку сообщений
# 
# ---------------------------------------------------------------------------
# OSError                                   Traceback (most recent call last)
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
#     599                                                   body=body, headers=headers,
# --> 600                                                   chunked=chunked)
#     601 
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
#     383                     # otherwise it looks like a programming error was the cause.
# --> 384                     six.raise_from(e, None)
#     385         except (SocketTimeout, BaseSSLError, SocketError) as e:
# 
# /usr/lib/python3/dist-packages/six.py in raise_from(value, from_value)
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
#     379                 try:
# --> 380                     httplib_response = conn.getresponse()
#     381                 except Exception as e:
# 
# /usr/lib/python3.7/http/client.py in getresponse(self)
#    1335             try:
# -> 1336                 response.begin()
#    1337             except ConnectionError:
# 
# /usr/lib/python3.7/http/client.py in begin(self)
#     305         while True:
# --> 306             version, status, reason = self._read_status()
#     307             if status != CONTINUE:
# 
# /usr/lib/python3.7/http/client.py in _read_status(self)
#     266     def _read_status(self):
# --> 267         line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
#     268         if len(line) > _MAXLINE:
# 
# /usr/lib/python3.7/socket.py in readinto(self, b)
#     588             try:
# --> 589                 return self._sock.recv_into(b)
#     590             except timeout:
# 
# /usr/lib/python3/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
#     308             else:
# --> 309                 return self.recv_into(*args, **kwargs)
#     310 
# 
# /usr/lib/python3/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
#     298             else:
# --> 299                 raise SocketError(str(e))
#     300         except OpenSSL.SSL.ZeroReturnError as e:
# 
# OSError: (104, 'ECONNRESET')
# 
# During handling of the above exception, another exception occurred:
# 
# ProtocolError                             Traceback (most recent call last)
# <ipython-input-5-81f9a05c227a> in <module>
#      64                 print('\n{}: начинаю отправку сообщений\n'.format(datetime.today()))
#      65                 for file_name in files_list:
# ---> 66                     send_data_to_tlg(file_name)
#      67                 print('\n{}: сообщения отправлены\n'.format(datetime.today()))
#      68 
# 
# <ipython-input-2-060d59d2caf5> in send_data_to_tlg(file_name)
#      52     file_extension = file_name.split('.')[1] # расширение файла
#      53     if file_extension == 'txt':
# ---> 54         send_message_to_tlg(file_name)
#      55         print('{}: send text {}'.format(datetime.today(), file_name))
#      56     elif file_extension == 'mov':
# 
# <ipython-input-2-060d59d2caf5> in send_message_to_tlg(file)
#      34     """Отправка сообщений в телеграмм"""
#      35     with open(os.path.join('data', file), 'r') as txt:
# ---> 36         bot.sendMessage(bs.chat_id, txt.read())
#      37 
#      38 
# 
# ~/.local/lib/python3.7/site-packages/telepot/__init__.py in sendMessage(self, chat_id, text, parse_mode, disable_web_page_preview, disable_notification, reply_to_message_id, reply_markup)
#     511         """ See: https://core.telegram.org/bots/api#sendmessage """
#     512         p = _strip(locals())
# --> 513         return self._api_request('sendMessage', _rectify(p))
#     514 
#     515     def forwardMessage(self, chat_id, from_chat_id, message_id,
# 
# ~/.local/lib/python3.7/site-packages/telepot/__init__.py in _api_request(self, method, params, files, **kwargs)
#     489 
#     490     def _api_request(self, method, params=None, files=None, **kwargs):
# --> 491         return api.request((self._token, method, params, files), **kwargs)
#     492 
#     493     def _api_request_with_file(self, method, params, file_key, file_value, **kwargs):
# 
# ~/.local/lib/python3.7/site-packages/telepot/api.py in request(req, **user_kw)
#     152 def request(req, **user_kw):
#     153     fn, args, kwargs = _transform(req, **user_kw)
# --> 154     r = fn(*args, **kwargs)  # `fn` must be thread-safe
#     155     return _parse(r)
#     156 
# 
# /usr/lib/python3/dist-packages/urllib3/request.py in request_encode_body(self, method, url, fields, headers, encode_multipart, multipart_boundary, **urlopen_kw)
#     148         extra_kw.update(urlopen_kw)
#     149 
# --> 150         return self.urlopen(method, url, **extra_kw)
# 
# /usr/lib/python3/dist-packages/urllib3/poolmanager.py in urlopen(self, method, url, redirect, **kw)
#     321             response = conn.urlopen(method, url, **kw)
#     322         else:
# --> 323             response = conn.urlopen(method, u.request_uri, **kw)
#     324 
#     325         redirect_location = redirect and response.get_redirect_location()
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
#     636 
#     637             retries = retries.increment(method, url, error=e, _pool=self,
# --> 638                                         _stacktrace=sys.exc_info()[2])
#     639             retries.sleep()
#     640 
# 
# /usr/lib/python3/dist-packages/urllib3/util/retry.py in increment(self, method, url, response, error, _pool, _stacktrace)
#     365             # Read retry?
#     366             if read is False or not self._is_method_retryable(method):
# --> 367                 raise six.reraise(type(error), error, _stacktrace)
#     368             elif read is not None:
#     369                 read -= 1
# 
# /usr/lib/python3/dist-packages/six.py in reraise(tp, value, tb)
#     690                 value = tp()
#     691             if value.__traceback__ is not tb:
# --> 692                 raise value.with_traceback(tb)
#     693             raise value
#     694         finally:
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
#     598                                                   timeout=timeout_obj,
#     599                                                   body=body, headers=headers,
# --> 600                                                   chunked=chunked)
#     601 
#     602             # If we're going to release the connection in ``finally:``, then
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
#     382                     # Remove the TypeError from the exception chain in Python 3;
#     383                     # otherwise it looks like a programming error was the cause.
# --> 384                     six.raise_from(e, None)
#     385         except (SocketTimeout, BaseSSLError, SocketError) as e:
#     386             self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
# 
# /usr/lib/python3/dist-packages/six.py in raise_from(value, from_value)
# 
# /usr/lib/python3/dist-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
#     378             except TypeError:  # Python 3
#     379                 try:
# --> 380                     httplib_response = conn.getresponse()
#     381                 except Exception as e:
#     382                     # Remove the TypeError from the exception chain in Python 3;
# 
# /usr/lib/python3.7/http/client.py in getresponse(self)
#    1334         try:
#    1335             try:
# -> 1336                 response.begin()
#    1337             except ConnectionError:
#    1338                 self.close()
# 
# /usr/lib/python3.7/http/client.py in begin(self)
#     304         # read until we get a non-100 response
#     305         while True:
# --> 306             version, status, reason = self._read_status()
#     307             if status != CONTINUE:
#     308                 break
# 
# /usr/lib/python3.7/http/client.py in _read_status(self)
#     265 
#     266     def _read_status(self):
# --> 267         line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
#     268         if len(line) > _MAXLINE:
#     269             raise LineTooLong("status line")
# 
# /usr/lib/python3.7/socket.py in readinto(self, b)
#     587         while True:
#     588             try:
# --> 589                 return self._sock.recv_into(b)
#     590             except timeout:
#     591                 self._timeout_occurred = True
# 
# /usr/lib/python3/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
#     307                 raise timeout('The read operation timed out')
#     308             else:
# --> 309                 return self.recv_into(*args, **kwargs)
#     310 
#     311     def settimeout(self, timeout):
# 
# /usr/lib/python3/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
#     297                 return 0
#     298             else:
# --> 299                 raise SocketError(str(e))
#     300         except OpenSSL.SSL.ZeroReturnError as e:
#     301             if self.connection.get_shutdown() == OpenSSL.SSL.RECEIVED_SHUTDOWN:
# 
# ProtocolError: ('Connection aborted.', OSError("(104, 'ECONNRESET')"))
# 
# 

# In[ ]:




