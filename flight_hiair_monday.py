from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
import telegram
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cralwer_flight_hiair_monday import exract_flight_hiair_monday

now = datetime.datetime.today() + datetime.timedelta(hours=9)

print(now)

delta = 0 - now.weekday()
if delta <= 0:
    delta = 7 - now.weekday()

friday = [0, 0, 0, 0, 0]
friday[0] = now
friday[1] = friday[0] + datetime.timedelta(days=delta)
friday[2] = friday[1] + datetime.timedelta(days=7)
friday[3] = friday[2] + datetime.timedelta(days=7)
friday[4] = friday[3] + datetime.timedelta(days=7)

friday_month = [0, 0, 0, 0, 0]

j = 0
while j<4:
    if friday[0].month != friday[j+1].month:
       friday_month[j+1] = 1
    else:
       friday_month[j+1] = 0
    j = j+1

first_content = exract_flight_hiair_monday(str(friday[1].day), friday_month[1])
second_content = exract_flight_hiair_monday(str(friday[2].day), friday_month[2])
third_content = exract_flight_hiair_monday(str(friday[3].day), friday_month[3])
fourth_content = exract_flight_hiair_monday(str(friday[4].day), friday_month[4])

first_content.insert(0,friday[1].strftime('%Y-%m-%d'))
second_content.insert(0,friday[2].strftime('%Y-%m-%d'))
third_content.insert(0,friday[3].strftime('%Y-%m-%d'))
fourth_content.insert(0,friday[4].strftime('%Y-%m-%d'))

total_content = first_content + second_content + third_content + fourth_content
total_content_clean = '\n'.join(total_content)
 
bot = telegram.Bot(token=os.environ.get('telegram_token'))
chat_id = 1491027495 #bot.getUpdates()[-1].message.chat.id

bot.sendMessage(chat_id=chat_id, text=total_content_clean)
