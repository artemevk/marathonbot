#!/usr/bin/env python
# coding: utf-8

#--------------------Настройки бота-------------------------
# Ваш токен от BotFather
token = '1318094188:AAEpy6lDo4Ld5FwPyvY6vQGDsncVKGvo148'

# ID владельца бота
owner_id = 242076979

# ID чата в который отправлять сообщения
chat_id = -1001480357109

# День начала марафона
start_day = '09.10.2020'

# День окончания марафона
finish_day = '12.10.2020'

# Час отправки сообщений в чат
send_hour = 10

# Ссылки на материалы - (одна ссылка = один день)
links = [['https://yadi.sk/d/pN4VURbpttmJnw', 'https://yadi.sk/i/xCbt-CkKMutgIA', 
          'https://yadi.sk/d/K3d3uroPcC78OA', 'https://yadi.sk/i/BVn4QqGrroAEDQ'],
         ['https://yadi.sk/d/scW105GwB_itbA', 'https://yadi.sk/d/aJdFuz9VKJ3gfQ',
          'https://yadi.sk/d/MPVk50xbZfDWSw', 'https://yadi.sk/d/WD7_7yoj-sSkSA',
          'https://yadi.sk/d/iPgkYrRUEOam0w', 'https://yadi.sk/d/WJQnFHNyuCKiRA', 
          'https://yadi.sk/d/UeCyy1oeTFg4ag', 'https://yadi.sk/i/WwWZ49U1syuu-w',
          'https://yadi.sk/d/SByELgROILEMig'], 
         ['https://yadi.sk/d/nnRbWnVZjm6iBA', 'https://yadi.sk/d/UyQY_L0B-3sUDA',
          'https://yadi.sk/d/zMj3obb8WmS6Sg', 'https://yadi.sk/d/u_iUaQ7rMHf2ww',
          'https://yadi.sk/d/hiX42g19BSD16w', 'https://yadi.sk/d/k9h0zJYn8bgOKw',
          'https://yadi.sk/d/wEJtIpK4wN8zOg', 'https://yadi.sk/d/T7GwBTsvrd3hew',
          'https://yadi.sk/d/f6_mtIswChBKfQ', 'https://yadi.sk/d/WIYLj0AMDCVsoQ'], 
         ['https://yadi.sk/d/C0FiVIwH_roolw', 'https://yadi.sk/d/Kr_ZDbWPIUeUOA',
          'https://yadi.sk/d/Uj_LWu70UEhh2g', 'https://yadi.sk/d/MqJ6JIw5ZW3cmA',
          'https://yadi.sk/d/i0qSzqnXXW_OSA', 'https://yadi.sk/i/4o8WsT3zVHf4vA',
          'https://yadi.sk/d/I7zJsF4aYV9L5Q', 'https://yadi.sk/i/K2Xs2FPOwM4OEA',
          'https://yadi.sk/i/vclrs87Mmsv7gg', 'https://yadi.sk/i/TdE8ZiS3ZMMTAg',
          'https://yadi.sk/d/RiFln96yIux9qw'],
         ['https://yadi.sk/d/ILjV3oCY-zgjXw', 'https://yadi.sk/d/IG-x0HCX7LJeXg',
          'https://yadi.sk/d/DOaB4Ale1EgFBg', 'https://yadi.sk/d/OA-572qlP6Hj_A',
          'https://yadi.sk/d/5UqoolewSG-_JQ', 'https://yadi.sk/d/bCoaCZ-hYfisdg',
          'https://yadi.sk/d/q31yGV_IY_rQ0w'],
         ['https://yadi.sk/d/AcaBFD147xX3Ig']
        ]

# Логирование
# logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token=token)
# dp = Dispatcher(bot)
#
# # Ваш айди аккаунта администратора и айди сообщения где хранится файл с данными
# admin_id=12345678
# config_id=12345
#
# conn = sqlite3.connect(":memory:")  # настройки in memory бд
# cursor = conn.cursor()