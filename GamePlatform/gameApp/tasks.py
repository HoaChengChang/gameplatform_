from celery import shared_task
import time
import datetime
import threading
import queue



def save_to_database(data_list: list = None):  # 皓程
    from gameApp.models import Game, GamePlatform, Classification, GameType, GamePlatformRelation, GameTypeRelation
    if not data_list:
        return
    '''
    由於要降低DB的負荷，所以使用bulk_create批次存入資料庫，
    又加上有物件有foreignkey,manytomany關係，寫法才會如下：
    '''
    platform, _ = GamePlatform.objects.get_or_create(name=data_list[0]["platform"][0],
                                                    loge_picture=data_list[0]["platform_logo_path"])
    game_classification_limit, _ = Classification.objects.get_or_create(class_name=1)
    game_classification_commen, _ = Classification.objects.get_or_create(class_name=0)

    for item in data_list:
        if item["release_date"] in (None, ""):
            item["release_date"] = datetime.date.today()

    result_game = [Game(
        name=item["game_name"],
        introduction=item["introduction"],
        hardware_or_fileinfo=item["hardware_need"],
        game_classification=game_classification_limit,
        release_date=item["release_date"],
        pay=item["pay"],
        picture_game=item["picture_path"],
        url_address=item["web_address"],
        game_type_tmp=','.join(item["type"])
    ) if item["classification"] == 1 else
        Game(
        name=item["game_name"],
        introduction=item["introduction"],
        hardware_or_fileinfo=item["hardware_need"],
        game_classification=game_classification_commen,
        release_date=item["release_date"],
        pay=item["pay"],
        picture_game=item["picture_path"],
        url_address=item["web_address"],
        game_type_tmp=','.join(item["type"])
    ) for item in data_list]

    created_games = Game.objects.bulk_create(result_game)

    #重新抓取game，如果直接用result_game是沒辦法匯進去GamePlatformRelation、GameTypeRelation
    saved_games = Game.objects.filter(name__in = [game.name for game in created_games])
    result_platform = [GamePlatformRelation(game = game, platform = platform) for game in saved_games]
    
    #game_type from char to object
    result_GameTypeRelation = []
    for game in saved_games:
        if len(game.game_type_tmp.split(',')) == 1:
            game_type, _ = GameType.objects.get_or_create(
                typename=game.game_type_tmp)
            result_GameTypeRelation.append(
                GameTypeRelation(game=game, game_type=game_type))
        else:
            game_type_list = [GameType.objects.get_or_create(typename=game_type)[0]
                              for game_type in game.game_type_tmp.split(',')]
            for game_type_obj in game_type_list:
                result_GameTypeRelation.append(
                    GameTypeRelation(game=game, game_type=game_type_obj))

    GameTypeRelation.objects.bulk_create(result_GameTypeRelation)
    GamePlatformRelation.objects.bulk_create(result_platform)


def megagames():#爬蟲：皓程
    from gameApp.crawler.megagames import Crawl_megagames
    results = Crawl_megagames()
    save_to_database(results)


def oceanofGames():#爬蟲：宗錡
    from gameApp.crawler.Ocean import OceanOfGames
    results = OceanOfGames()
    save_to_database(results)


def SteamGames():
    from crawler.miyuuuu_Crawl.steam_main import Crawl_Steam

    steam_cate = ['action', 'arcade_rhythm', 'shmup', 'action_fps', 'action_tps',
                  'adventure', 'casual', 'adventure_rpg', 'story_rich',
                  'rpg', 'adventure_rpg', 'rpg_action', 'rpg_turn_based', 'rpg_party_based', 'rpg_jrpg', 'rpg_strategy_tactics',
                  'simulation', 'sim_hobby_sim', 'sim_life', 'action_run_jump',
                  'strategy_card_board', 'strategy_real_time', 'strategy_turn_based',
                  'sports_and_racing', 'strategy_grand_4x', 'sports_individual', 'sports_team', 'sports',
                  'racing', 'racing_sim', 'sports_sim']

# Crawl_Steam(<category>, <More Button Count>, <Error Chance>)
# category is steam category
# More Button Count ( value 0 ＝ ∞ )
# Error Chance
#   ec = -1     No more button.
#   ec = 0      No error chance.    （default）
#   ec = <int>  Error chance count. （no debug）

    for i in steam_cate:
        results = Crawl_Steam(i, 60)
        save_to_database(results)


def epicgames():#爬蟲：英帆
    from gameApp.crawler.Epic import crawl_epicgames
    results = crawl_epicgames(1000)
    save_to_database(results)


def battlenetgames():#爬蟲：崇皓
    from gameApp.crawler.battlenet import get_battle
    results = get_battle()
    save_to_database(results)



class Crawlfactory: #皓程
    def __init__(self, num_threads : int): 
        self.num_threads = num_threads
        self.tasks = queue.Queue()
        self.threads = []
    #加任務（函式）
    def add_tasks(self, task_list : list):
        for task in task_list:
            self.tasks.put(task)

    def worker(self): 
        while not self.tasks.empty():
            task = self.tasks.get()
            if task is None:
                break
            task() 
            self.tasks.task_done()

    def start_processing(self):
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker)  
            self.threads.append(thread)
            thread.start()
        for thread in self.threads:
            #等到所有任務皆完成，start_processing才真正結束
            thread.join()


@shared_task
def work_chain(): #皓程
    '''
    針對5個平台進行爬蟲，由於selenium是由docker架在虛擬機上，
    虛擬機效能有限，所以只開 2 threads
    '''
    tasks = Crawlfactory(2)
    tasks.add_tasks([megagames, oceanofGames, SteamGames, epicgames, battlenetgames])
    tasks.start_processing()

