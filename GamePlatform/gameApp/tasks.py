from celery import shared_task
import time
import datetime
import threading
import queue

def save_to_database(data_list : list = None):  #皓程
    from gameApp.models import Game,GamePlatform,Classification,GameType,GamePlatformRelation,GameTypeRelation
    if not data_list:
        return
    platform, _ = GamePlatform.objects.get_or_create(name = data_list[0]["platform"][0], loge_picture = data_list[0]["platform_logo_path"])
    game_classification_limit, _ = Classification.objects.get_or_create(class_name = 1)
    game_classification_commen, _ = Classification.objects.get_or_create(class_name = 0)

    for item in data_list:
        if item["release_date"] in (None, ""):
            item["release_date"] = datetime.date.today()
            
    result_game = [Game(
        name = item["game_name"],
        introduction = item["introduction"],
        hardware_or_fileinfo = item["hardware_need"],
        game_classification = game_classification_limit,
        release_date = item["release_date"],
        pay = item["pay"],
        picture_game = item["picture_path"],
        url_address = item["web_address"],
        game_type_tmp =  ','.join(item["type"])
    ) if item["classification"] == 1 else
        Game(
        name = item["game_name"],
        introduction = item["introduction"],
        hardware_or_fileinfo = item["hardware_need"],
        game_classification = game_classification_commen,
        release_date = item["release_date"],
        pay = item["pay"],
        picture_game = item["picture_path"],
        url_address = item["web_address"],
        game_type_tmp = ','.join(item["type"])
    ) for item in data_list ]
    
    created_games = Game.objects.bulk_create(result_game)
    #重新抓取game，如果直接用result_game是沒辦法匯進去GamePlatformRelation、GameTypeRelation
    saved_games = Game.objects.filter(name__in = [game.name for game in created_games])
    result_platform = [GamePlatformRelation(game = game, platform = platform) for game in saved_games]
    
    #game_type from char to object
    game_type_list = []
    result_GameTypeRelation = []
    for game in saved_games:
        if len(game.game_type_tmp.split(',')) == 1:
            game_type, _ = GameType.objects.get_or_create(typename = game.game_type_tmp)
            result_GameTypeRelation.append(GameTypeRelation(game = game, game_type = game_type))
        else:
            game_type_list = [GameType.objects.get_or_create(typename = game_type)[0] 
                              for game_type in game.game_type_tmp.split(',')]
            for game_type_obj in game_type_list:
                result_GameTypeRelation.append(GameTypeRelation(game = game, game_type = game_type_obj))
    
    GameTypeRelation.objects.bulk_create(result_GameTypeRelation)
    GamePlatformRelation.objects.bulk_create(result_platform)

def megagames():
    from gameApp.crawler.megagames import Crawl_megagames
    results = Crawl_megagames()
    save_to_database(results)

def oceanofGames():
    pass
    # from gameApp.crawler.Ocean import OceanOfGames
    # results = OceanOfGames()
    # save_to_database(results)

    
def C():
    try:
        for _ in range(20):
            print("C")
            time.sleep(1)
    finally:
        pass

def D():
    try:
        for _ in range(20):
            print("D")
            time.sleep(1)
    finally:
        pass

def E():
    try:
        for _ in range(20):
            print("E")
            time.sleep(1)
    finally:
        pass


class Crawlfactory:
    def __init__(self, num_threads : int): #chrome_browser : webdriver
        # self.browser = chrome_browser
        self.num_threads = num_threads
        self.tasks = queue.Queue()
        self.threads = []
    def add_tasks(self, task_list : list):
        for task in task_list:
            self.tasks.put(task)
    def worker(self): #brw : webdriver
        while not self.tasks.empty():
            task = self.tasks.get()
            if task is None:
                break
            task() #brw 
            self.tasks.task_done()

    def start_processing(self):
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker)  #args=(self.browser,)
            self.threads.append(thread)
            thread.start()    
        for thread in self.threads:
            thread.join()
            # self.browser.quit()
       
        


        
    
@shared_task
def work_chain():

    # chrome_browser = webdriver.Remote(
    #     command_executor='http://35.240.205.111:4444/wd/hub',
    #     options=webdriver.ChromeOptions()
    # )
    # firefox_browser = webdriver.Remote(
    #     command_executor='http://35.240.205.111:4444/wd/hub',
    #     options=webdriver.FirefoxOptions()
    # )
    
    tasks = Crawlfactory(2)#chrome_browser,
    tasks.add_tasks([megagames,oceanofGames,C,D,E])
    tasks.start_processing()
    # task_chain = chain(
    #     MegaGames.s(),
    #     B.s(),
    #     C.s(),
    #     D.s(),
    #     E.s(),
    # )
    # return task_chain()