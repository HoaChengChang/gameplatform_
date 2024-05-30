from typing import Dict, Any

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd


def crawl():
    games = []
    try:
        driver = webdriver.Remote(
            command_executor='http://125.229.236.88:55444/wd/hub',
            options=webdriver.ChromeOptions()
        )
        driver.get("https://oceanofgames.com/")
        gen = {"Action": "動作", "Adventure": "冒險", "Arcade": "大型電玩", "Fighting": "格鬥", "Horror": "恐怖",
               "Puzzle": "益智", "Racing": "駕駛", "Shooting Games": "射擊", "Simulation": "模擬", "Sports": "體育",
               "War": "戰略", "Strategy": "戰略", "Mystery": "冒險", "Fantasy": "冒險", "Sci Fi": "冒險", "RPG": "RPG",
               "Survival": "模擬", "Casual": "模擬", "Indie": "獨立", "Reviews": "not in type",
               "Trainer": "not in type"}
        while len(games) <= 20:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.post-details')))
            contents = driver.find_element(By.XPATH,
                                           "/html/body/div/div/div[2]/div/div/div/div/div[1]/div/div[1]").find_elements(
                By.CSS_SELECTOR, "div.post-details")
            time.sleep(0.2)
            for content in contents:
                c_a = ''
                try:
                    c_a = content.find_element(By.TAG_NAME, "a")
                except StaleElementReferenceException:
                    time.sleep(0.5)
                if c_a == '':
                    continue
                print(c_a.get_attribute("title"))  # 遊戲名
                print(c_a.get_attribute("href"))  # 頁面鏈接
                game = {"game_name": '', "introduction": '', "hardware_need": '', "platform": [], "type": [],
                        "release_date": None, "pay": False, "picture_path": '', "web_address": '', "classification": 0,
                        "platform_logo_path": '/images/Ocean.png'}
                game["game_name"] = c_a.get_attribute("title").split(" Free Download")[0]
                game["web_address"] = c_a.get_attribute("href")
                game["platform"].append("Ocean of games")
                try:
                    c_img = content.find_element(By.TAG_NAME, "img")
                    print(c_img.get_attribute("src"))  # 封面圖片)
                    game["picture_path"] = c_img.get_attribute("src")
                except NoSuchElementException:
                    print("no image")
                c_g = content.find_element(By.CSS_SELECTOR, "div.post-info")
                print(c_g.text.split("in ")[-1].split(", "))  # 遊戲分類
                GENRES = c_g.text.split("in ")[-1].split(", ")
                if "Reviews" in GENRES or "Trainer" in GENRES:  # 若類型不符要求則跳過
                    continue
                else:
                    for GEN in GENRES:
                        game["type"].append(gen[GEN])
                c_a.click()  # 點擊該遊戲
                time.sleep(0.7)
                try:
                    dis = driver.find_element(By.XPATH,
                                              "/html/body/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/div[1]/p[1]")
                except NoSuchElementException:
                    continue
                print(dis.text)  # 遊戲描述
                game["introduction"] = dis.text
                s_reqs = driver.find_elements(By.CSS_SELECTOR, "ul")
                for s_req in s_reqs:
                    if "GPU" in s_req.text or "Graphics" in s_req.text and "Memory" in s_req.text:
                        req = s_req.text
                        print(req)  # 系統需求
                        game["hardware_need"] = req
                        break

                s_reqs = driver.find_elements(By.CSS_SELECTOR, "p")
                for s_req in s_reqs:
                    if "GPU" in s_req.text or "Graphics" in s_req.text and "Memory" in s_req.text:
                        req = s_req.text
                        print(req)  # 系統需求
                        game["hardware_need"] = req
                        break
                games.append(game)
                print()
                driver.back()
            print()
            try:
                driver.find_element(By.CSS_SELECTOR, "a.next").click()
            except NoSuchElementException:
                pass
    finally:
        driver.quit()
        return games


def OceanOfGames():
    games: list = crawl()
    while not games:
        crawl()
    return games
