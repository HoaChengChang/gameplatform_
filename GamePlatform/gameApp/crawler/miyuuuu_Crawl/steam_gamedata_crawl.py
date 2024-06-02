#encoding=utf-8

from time import sleep as wait
# from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Steam_Category_changer import Category_change as TypeChange

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
# ua = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.237 Safari/534.10"

# def NoError_EnName(link):
#     if link[-1] == "/":
#         link = link[:-1]
#     try:
#         name = link.split("/")[-1].split("?")[0] 
#     except:
#         try:
#             return link.split("/")[-1]
#         except:
#             return 
#     else:
#         return name

def gamedata(url, IsData='Project'):

# Use local
    # opts = Options()

# Use Selenium Grid
    opts = webdriver.ChromeOptions()

    opts.add_argument("--incognito")
    opts.add_argument("--window-size=1200,1080")
    opts.add_argument("--handless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("user-agent="+ua)

# Use Selenium Grid
    driver = webdriver.Remote(
    # command_executor='http://35.240.205.111:4444/wd/hub',
    # command_executor='https://sngrid.miyuuuu.me/wd/hub',
    command_executor='http://125.229.236.88:55444/wd/hub',
    # command_executor='http://172.16.8.5:4444/wd/hub',
    options=opts)

# Use local
    # driver = webdriver.Chrome(options=opts)
    driver.get(url)
    wait(2)

    try:
        driver.find_element(By.ID, 'appHubAppName').text
    except:
        # Birth18 = driver.find_element(By.XPATH, '//*[@class="agegate_birthday_selector"]')
        Classificate = 1
        ageDay = Select(driver.find_element(By.ID, 'ageDay'))
        ageDay.select_by_value("1")
        wait(0.7)
        ageMonth = Select(driver.find_element(By.ID, 'ageMonth'))
        ageMonth.select_by_index(0)
        wait(0.7)
        ageYear = Select(driver.find_element(By.ID, 'ageYear'))
        ageYear.select_by_value("2000")
        wait(0.7)
        OkButton = driver.find_element(By.ID, 'view_product_page_btn')
        OkButton.click()
        wait(3.3)
    else:
        Classificate = 0

# debug
    # print(url)

# Page language switch to Chinese
    driver.find_element(By.ID, 'language_pulldown').click()
    wait(1)
    driver.find_element(By.XPATH, '//*[@id="language_dropdown"]/div/a[2]').click()

# Scroll
    wait(6)
    driver.execute_script("var q=document.documentElement.scrollTop=300")

# Game Chinese Name
    AppName = driver.find_element(By.ID, 'appHubAppName').text

# Game English Name
    # EnAppName = (NoError_EnName(url) if NoError_EnName(url)[0] != '_' else NoError_EnName(url)[1:]).replace("_", " ")
    # returnData.append(EnAppName)

# Game If need price?
    
    try:
        Is_Price = driver.find_element(By.XPATH, '//*[@id="game_area_purchase"]//*[@class="game_purchase_price price"]').text
    except:
        Is_Price = driver.find_element(By.XPATH, '//*[@id="game_area_purchase"]//*[@class="discount_original_price"]').text

    if '免費' in Is_Price:
        pay = False
    else:
        pay = True

# Game logo link
    # logoLink = driver.find_element(By.CSS_SELECTOR, 'img.game_header_image_full ').get_attribute('src')

# Game url link
    Url = url

# Game release date
    ReleaseDate = driver.find_element(By.CSS_SELECTOR, '.glance_ctn .release_date .date').text
    ReleaseDate = ReleaseDate.replace(' ', '').replace('年', '-').replace('月', '-').replace('日', '')

# Game Movie
    # try:
    #     m = driver.find_elements(By.XPATH, '//*[@id="highlight_player_area"]//*[contains(@id,"highlight_movie_")]')
    # except:
    #     Movie = None
    #     print('movieno')
    # else:
    #     Movie = []
    #     for i in m:
    #         Movie.append(i.get_attribute('data-mp4-hd-source'))

# Game picture link
    BigpicLink = []
    pl = driver.find_elements(By.CSS_SELECTOR, '.screenshot_holder > a')
    for i in pl:
        BigpicLink.append(i.get_attribute("href"))
        wait(0.5)

# Game develop
    # Develop = []
    # deve = driver.find_elements(By.XPATH, '//*[@class="dev_row"]/*[@id="developers_list"]/a')
    # for i in deve:
    #     Develop.append(i.text)

# Game publish
    # publish = driver.find_element(By.XPATH, '//*[@class="dev_row"]/*[@class="summary column"]/a[contains(@href,"publisher")]').text

# Game review
    Game_Review = driver.find_element(By.ID, 'game_area_description').text

# Game spec
    Spec = driver.find_element(By.XPATH, '//*[@class="game_page_autocollapse sys_req"]').text

# Game category
    Category = []
    ctgr = driver.find_elements(By.XPATH, '//*[@id="genresAndManufacturer"]//*[contains(@href,"https://store.steampowered.com/genre/")]')
    for i in ctgr:
        Category.append(i.text)

# Game tag
    Tag = []

    # tg = driver.find_elements(By.XPATH, '//*[@class="glance_tags popular_tags"]/a')
    # tg = driver.find_elements(By.CLASS_NAME, 'app_tag')
    # tg = driver.find_elements(By.CSS_SELECTOR, '.app_tag')

    # for i in tg:
    #     Tag.append(i.text)
    # print(Tag)

#Game tag Plus

    driver.find_element(By.XPATH, '//*[@class="glance_tags popular_tags"]/div').click()
    wait(0.8)
    tgp = driver.find_elements(By.XPATH, '//*[@class="newmodal app_tag_modal_frame"]//*[@class="app_tags popular_tags"]/div/a')
    wait(0.8)

    for i in tgp:
        Tag.append(i.text)

    # if '成人' in Tag:
    #     Classificate = 1
    # elif '色情' in Tag:
    #     Classificate = 1
    # elif 'Hentai' in Tag:
    #     Classificate = 1
    # else:
    #     Classificate = 0

    # print(Tag)

    driver.find_element(By.XPATH, '//*[@class="newmodal_buttons"]/div').click()
    wait(0.6)

# Category and Tag change for Steam Types
    catetag = set()
    for i in Category+Tag:
        # catetag.add(j for j in TypeChange(i))
        for j in TypeChange(i):
            catetag.add(j)

    Types = [ct for ct in catetag]
    # if Is18 == True:
    #     Types.append('18禁')

    driver.quit()

    SteamLogo = "https://store.cloudflare.steamstatic.com/public/shared/images/header/logo_steam.svg?t=962016"

    if IsData == 'Project':
        return dict(game_name=AppName,
            introduction=Game_Review,
            hardware_need=Spec,
            platform=['STEAM'],
            type=Types,
            display_time=ReleaseDate,
            pay=pay,
            picture_path=BigpicLink[0],
            web_address=Url,
            classification=Classificate,
            platform_logo_path=SteamLogo,
            )
    elif IsData == 'Types':
        return Types

# ------------------------------------------------------------------------------

# test
if __name__ == "__main__":
    import json
    # gameurl = "https://store.steampowered.com/app/1973710/_Heaven_Burns_Red/"
    gameurl = "https://store.steampowered.com/app/1649240/Returnal?snr=1_category_4_arcaderhythm_salebrowseall"
    # gameurl = "https://store.steampowered.com/app/2106670/_/"
    # gameurl = "https://store.steampowered.com/app/1091500/Cyberpunk_2077/"

    SteamGames = []

    gd = gamedata(gameurl)
    SteamGames.append(gd)
    gddump = json.dumps(SteamGames, ensure_ascii=False, indent=4)
    print(gddump)
