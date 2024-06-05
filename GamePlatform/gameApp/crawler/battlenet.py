from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 抓取連結
def get_battle():
    driver = chrome_browser = webdriver.Remote(
            # command_executor='http://35.240.205.111:4444/wd/hub',
            command_executor='https://sngrid.miyuuuu.me/wd/hub',
            options=webdriver.ChromeOptions())
    # driver=webdriver.Chrome()
    driver.get("https://tw.shop.battle.net/zh-tw")
    driver.maximize_window()
    wait=WebDriverWait(driver, 10) 
    game_name=[]
    introduction=[]
    h_requirements=[]
    platform=[]
    types=[]
    pay=[]
    classification=[]
    web_address=[]
    imgs=[]
    output=[]
    datas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.browse-column.navigation-subnav')))
    # names18 = ["先鋒","現代戰爭","黑色行動","暗黑破壞神"]
    for d in datas:
        links = d.find_elements(By.TAG_NAME, 'a')
        for l in links:
            href = l.get_attribute('href')
            title = l.get_attribute('title')
            game_name.append(title)
            web_address.append(href)
            # for n in names18:
            #     if n in title:
            #         classification.append(1)
            #     else:
            #         classification.append(0)
            # print(f"LINK: {href}, TITLE: {title}")
    # 利用連結抓取內容
    try:
        for web in web_address:
            driver.get(web)
            if web != web_address[-3] and web != web_address[-2]:
                try:
                    find_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'browsing-card')))
                    find_a = find_div.find_element(By.TAG_NAME,'a')
                    href = find_a.get_attribute("href")
                    driver.get(href)
                except:
                    find_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'browsing-card-group')))
                    find_a = find_div.find_element(By.TAG_NAME,'a')
                    href = find_a.get_attribute("href")
                    driver.get(href)
            wait=WebDriverWait(driver, 10) 
            # print("介紹")
            intros = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.meka-font-body.product-heading__summary')))
            ilist=[]
            for i in intros:
                ilist+=i.text
            intro = ''.join(ilist)
            introduction.append(intro)
            # print(href_value)
            
            # print("需求")
            # syss=["Windows","Mac","iOS","Android"]
            result_re = ""
            find_div = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.system-requirements--tab")))
            for f in find_div:
                # device = f.find_elements(By.CSS_SELECTOR,'div.meka-tab')
                # for d in device:
                #     buttons = d.find_elements(By.TAG_NAME, "button")
                #     for b in buttons:
                #         actions = ActionChains(driver)
                #         actions.move_to_element(b).click().perform()
                #         # b.click()
                #         for s in syss:
                #             if s in d.text:
                result_re += "Windows" + "\n"
                # print(s)
                find_h3 = f.find_elements(By.TAG_NAME,'h3')
                for h3 in find_h3:
                    if h3.text!="":
                        result_re += h3.text + "\n"
                        # print(h3.text)
                    find_dt = f.find_elements(By.TAG_NAME,'dt')
                    find_dd = f.find_elements(By.TAG_NAME,'dd')
                    for dt,dd in zip(find_dt,find_dd):
                        if dt.text or dd.text !="":
                            result_re += dt.text + ":" + dd.text + "\n"
                            # print(dt.text+":"+dd.text)
            h_requirements.append(result_re)
            
            # print("平台")
            platform.append("Battle.net")
            
            # print("價格")
            temp_type=[]
            find_div = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.meka-button.meka-button--primary.meka-button--extra-large.ng-star-inserted")))
            for p in find_div:
                # print(p.text)
                if p.text =="免費暢玩":
                    pay.append(False)
                    temp_type.append("免費")
                else:
                    pay.append(True)
            
            # print("分級")
            find_div = driver.find_element(By.CLASS_NAME,'image')
            find_a = find_div.find_element(By.TAG_NAME,'img')
            alt = find_a.get_attribute("alt")
            if alt != "限制級":
                classification.append(0)
            else:
                classification.append(1)
            # print("分類")
            type_value={"射擊":"射擊","戰略":"戰略","冒險":"冒險","動作":"動作","角色扮演":"RPG","大型":"大型電玩"}
            find_cat = driver.find_element(By.CLASS_NAME,'name-category-container')
            p = find_cat.find_element(By.TAG_NAME, "p")
            for v in type_value:
                if v in p.text:
                    temp_type.append(type_value[v])
            types.append(temp_type)
            # for t in temp_type:
            #     print(t)
            
            # print("圖片")
            find_div = driver.find_element(By.CLASS_NAME,'swiper-slide.ng-star-inserted.swiper-slide-visible.swiper-slide-active')
            find_div = driver.find_element(By.CLASS_NAME,'feature.ng-star-inserted')                
            find_pic = find_div.find_element(By.TAG_NAME,'img')
            pic = find_pic.get_attribute("src")
            # print(pic)
            imgs.append(pic)
    
    
        for i in range(len(game_name)):
            game_temp = {
            "game_name": game_name[i],
            "introduction": introduction[i],
            "hardware_need": h_requirements[i],
            "platform": platform[i],
            "type": types[i],
            "release_date": "",
            "pay": pay[i],
            "picture_path": imgs[i],
            "web_address": web_address[i],
            "classification": classification[i],
            "platform_logo_path":"/statics/images/Battle.png"
            }
            output.append(game_temp)
        return(output)

    finally:        
            driver.quit()

get_battle()