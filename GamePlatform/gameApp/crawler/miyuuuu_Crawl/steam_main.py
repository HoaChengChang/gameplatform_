#encoding=utf-8

# --------setting--------

# Category Name
# categoryurl = 'action'
categoryurl = 'arcade_rhythm'
# categoryurl = 'soundtracks'

# More Button Count ( value 0 ＝ ∞ )
#   1 count ≒ 12 games
MBcount = 1

# Error Chance
#   ec = -1     No more button.
#   ec = 0      No error chance.
#   ec = <int>  Error chance count.

ec = -1

# ----------end----------

# import pandas as pd
# import numpy as np
import json
from time import sleep as wait
# from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from steam_gamedata_crawl import gamedata

def push_more(scroll=1358):
    more_button_css = "._2wLns48qa0uwOUf7ktqdsC ._3IRkbvGD9KD6DdmHo16WAl ._3d9cKhzXJMPBYzFkB_IaRp"
    global target 
    target= driver.find_element(By.CSS_SELECTOR, more_button_css)
    wait(0.6)
    target.click()
    wait(1.7)
    driver.execute_script(f'window.scrollBy(0,{str(scroll)})')
    wait(2)

def Crawl_Steam():
    mainurl = 'https://store.steampowered.com/category/'
    # suburl = '?facets13268=7%3A0%2C9%3A2%2C11%3A0'

    data_main_xpath = '//*[@id="SaleSection_13268"]//*[@class="NO-IPpXzHDNjw_TLDlIo7"]'

# Set User Agent and Privacy mode
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; zh-tw) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

    opts = webdriver.ChromeOptions()
    opts.add_argument("--incognito")
    opts.add_argument("--window-size=1200,1080")
    opts.add_argument("--handless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("user-agent="+ua)

# Set webdriver in Chrome and Get URL
    global driver
    driver = webdriver.Remote(
    # command_executor='http://35.240.205.111:4444/wd/hub',
    # command_executor='https://sngrid.miyuuuu.me/wd/hub',
    command_executor='http://125.229.236.88:55444/wd/hub',
    # command_executor='http://172.16.8.5:4444/wd/hub',
    options=opts
    )

    # driver = webdriver.Chrome(options=opts)
    driver.get(mainurl+categoryurl)
    wait(2.6)

# スクロール
    driver.execute_script("var q=document.documentElement.scrollTop=3530")
    wait(3)

# もっと表示ボタンのカウント
    if ec == -1:
        print('No push more mode.')

    elif ec == 0:
# No error Chance
        print('No error chance mode.')
        if MBcount == 0:
            while True:
                push_more()
        else:
            for i in range(MBcount):
                push_more()
    else:
# Is error Chance
        print('Is error chance mode.')
        for c in range(ec):
            try:
                if MBcount == 0:
                    while True:
                        push_more()
                else:
                    cMBc = MBcount
                    while cMBc > 0:
                        push_more()
                        cMBc -= 1
            except:
                for c2 in range(2):
                    if c2 == 0:
                        driver.execute_script(f'window.scrollBy(0,-280)')
                        wait(0.5)
                        try:
                            push_more()
                        except:
                            continue
                        else:
                            break
                    else:
                        driver.execute_script(f'window.scrollBy(0,95)')

                print(f'more button miss{c+1}')
                if c == ec-1:
                    print('no more button')

# リンク
    search_game_link = driver.find_elements(By.XPATH, f'{data_main_xpath}//*[@class="_1F4bcsKc9FjeWQ2TX8CWDe"]/a')
    GameLinks = []
    for sgl in search_game_link:
        url = sgl.get_attribute("href")
        GameLinks.append(url)
    # driver.close()
    driver.quit()

    '''
{"game_name":
    {
        "introduction":value,
        "hardware_need":value,
        "platform":[value],
        "type":[value],
        "display_time":value,
        "pay":True or False,
        "picture_path":value,
        "web_address":value,
        "classification":0 or 1,
    }
}
'''

# アウトプット
    SteamGames = []

    for gamelink in GameLinks:
        try:
            if gamedata(gamelink) != None:
                SteamGames.append(gamedata(gamelink))
            wait(0.3)
        except:
            wait(0.3)


    jdump = json.dumps(SteamGames, ensure_ascii=False, indent=4)

    print(jdump)

    # driver.quit()

    return SteamGames

if __name__ == "__main__":
    try:
        Crawl_Steam()
    except:
        print('Error.')
        driver.quit()
    finally:
        print('over')