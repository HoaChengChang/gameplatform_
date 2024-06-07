# -*- coding: utf-8 -*-
"""
Created on Fri May 17 21:27:52 2024

@author: fan19980129
"""

from selenium import webdriver
from bs4 import BeautifulSoup

def crawl_epicgames(total):
    gameList = []
    start = 0
    platform = "Epic Games"
    logoImg = "/images/Epic.png"
    typeDict = {"平台":"獨立","生存":"冒險","休閒":"益智","回合制":"益智",
         "回合策略":"戰略","多人線上戰鬥擂台":"競技","宇宙":"獨立","即時戰略":"戰略",
         "角色扮演":"RPG","奇幻":"冒險","冒險":"冒險","城塔防禦":"戰略",
         "城鎮建造":"模擬","拼圖":"益智","派對":"獨立","音樂":"獨立",
         "射擊":"射擊","恐怖":"恐怖","格鬥":"格鬥","益智問答":"益智",
         "紙牌遊戲":"益智","迷宮探索":"益智","動作":"動作","動作冒險":"動作",
         "探索":"冒險","敘事":"獨立","第一人稱":"模擬","復古":"獨立",
         "開放世界":"大型電玩","搞笑":"獨立","運動":"體育","模擬":"模擬",
         "潛行":"冒險","戰略":"戰略","獨立製作":"獨立","賽車":"駕駛","Rogue-lite":"RPG"} 

    while True:
        try:
            chrome_browser = webdriver.Remote(
            command_executor='http://sngrid.miyuuuu.me/wd/hub',
            options=webdriver.ChromeOptions())
            url = "https://store.epicgames.com/zh-Hant/browse?sortBy=releaseDate&sortDir=DESC&category=Game&count=40&start="+str(start)
            chrome_browser.get(url)
            soup = BeautifulSoup(chrome_browser.page_source, "html.parser")
            inUrls = soup.select("a.css-g3jcms")
            chrome_browser.quit()
            for inUrl in inUrls:
                gameDict = {"game_name":"","introduction":"","hardware_need":"","platform":[],"type":[],"release_date":"",
                            "pay":"","picture_path":"","web_address":"","classification":"","platform_logo_path":""}
                chrome_browser2 = webdriver.Remote(
                command_executor='http://sngrid.miyuuuu.me/wd/hub',
                options=webdriver.ChromeOptions())
                chrome_browser2.get("https://store.epicgames.com"+inUrl.get("href"))
                soup2 = BeautifulSoup(chrome_browser2.page_source, "html.parser")
                gameNames = soup2.select("span.css-1mzagbj")
                contents = soup2.select("div.css-1myreog")
                imgs = soup2.select("img.css-7i770w")
                pays = soup2.select("span.css-8en90x span")
                alts = soup2.select("img.css-bgy6b6")
                dates = soup2.select("span.css-119zqif time")
                gameTypes = soup2.select("li.css-t8k7")
                checks = soup2.select("div#panel-WINDOWS")
                itemLows = soup2.select("div.css-2sc5lq span.css-d3i3lr")[2::2]
                itemAdvices = soup2.select("div.css-2sc5lq span.css-d3i3lr")[3::2]
                needLows = soup2.select("div.css-2sc5lq span.css-119zqif")[::2]
                needAdvices = soup2.select("div.css-2sc5lq span.css-119zqif")[1::2]
                low = ""
                advice = ""
                
                for gameName,content,img,pay,date,alt,check in zip(gameNames,contents,imgs,pays,dates,alts,checks):
                    if pay.text == "即將推出":
                        continue
                    else:
                        gameDict["pay"] = pay.text == "立即購買"
                    gameDict["game_name"] = gameName.text
                    gameDict["introduction"] = content.text
                    for itemLow,needLow in zip(itemLows,needLows):
                        low += (itemLow.text+":"+needLow.text+"\n")
                    for itemAdvice,needAdvice in zip(itemAdvices,needAdvices):
                        advice += (itemAdvice.text+":"+needAdvice.text+"\n")
                    if "建議" in check.text:     
                        gameDict["hardware_need"] = "最低\n"+low+"\n"+"建議\n"+advice
                    gameDict["platform"].append(platform)
                    for gameType in gameTypes:
                        if gameType.text in typeDict and typeDict[gameType.text] not in gameDict["type"]:
                            gameDict["type"].append(typeDict[gameType.text])
                    gameDict["release_date"] = date.get("datetime").split("T")[0]
                    gameDict["picture_path"] = img.get("src")
                    gameDict["web_address"] = chrome_browser2.current_url
                    if alt.get("alt") == "18+":
                        gameDict["classification"] = 1
                    else:
                        gameDict["classification"] = 0
                    gameDict["platform_logo_path"] = logoImg
                if gameDict["game_name"] != "" and gameDict["hardware_need"] != "":
                    gameList.append(gameDict)
                chrome_browser2.quit()        
                if len(gameList) == total:
                    return gameList   
            start += 40
        finally:
            pass
            # chrome_browser.quit()
    





