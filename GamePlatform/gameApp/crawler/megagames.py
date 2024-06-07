import time
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import datetime
import threading
import queue


def Crawl_megagames():  #皓程
    from gameApp.models import Game 
    url = 'https://megagames.com/freeware'  
    data_list = []
    while True:
        browser = webdriver.Remote(
            command_executor='http://sngrid.miyuuuu.me/wd/hub',
            options=webdriver.ChromeOptions()
        )   
        try:
            browser.get(url)
            locator = (By.CLASS_NAME, 'pane-content')
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))
            pageSource = browser.page_source
            soup = BeautifulSoup(pageSource,'html.parser')
            games = soup.select("div.views-row-responsive.views-row")
            for item in games:
                data ={}
                platform_logo_path = "https://megagames.com/sites/all/themes/zentropy_mg/logo.png"
                soup2 = BeautifulSoup(str(item),'html.parser')
                url = 'https://megagames.com'+soup2.select_one("a").get('href')
                game_picture = soup2.select_one("img").get('src')
                game_name = soup2.select_one("div.views-field.views-field-title span.field-content").text
                sess = requests.Session()
                rPic = sess.get(url)
                soup3 = BeautifulSoup(rPic.text,'html.parser')
                game_introduction_list = soup3.select("div.field-item.even p")
                game_introduction = ''
                for i in game_introduction_list:
                    game_introduction += i.text + '\n'
                fileinfo_list = soup3.select("section.mg-content-block.file-info div.filename-info p") 
                fileinfo = ''
                for i in fileinfo_list:
                    fileinfo += i.text + '\n'
                post_time = soup3.select_one("div.post-date").text
                post_time = datetime.datetime.strptime(post_time, "%B %d, %Y - %I:%M%p").date()
                game = Game.objects.filter(name = game_name,
                                           introduction = game_introduction,
                                           hardware_or_fileinfo = fileinfo,
                                           release_date = str(post_time),
                                           picture_game = game_picture,
                                           url_address = url,
                                            )
                if game.exists(): #當第一筆資料存在，代表沒新遊戲，所以後面就不用處理了，這是因為要配合crontab
                    return data_list
                data = {
                    "game_name" : game_name,
                    "introduction" : game_introduction,
                    "hardware_need" : fileinfo,
                    "platform" : ["MegaGames"],
                    "type" : ["獨立","免費"],
                    "release_date" : str(post_time),
                    "pay" : False,
                    "picture_path" : game_picture,
                    "web_address" : url,
                    "platform_logo_path" : platform_logo_path,
                    "classification" : 1,
                }
                data_list.append(data)
                
            next_url = soup.select('li.pager-next a')
            print(next_url)
            if next_url == []:
                break
            else:
                url= 'https://megagames.com' + next_url[0].get('href')
                print(url)
        except:
            pass
        finally:
            browser.quit()
        #該頁處理完，先將資料存入資料庫
    return data_list