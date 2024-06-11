from celery import shared_task
import time
import datetime
import threading
import queue



def save_to_database(lock, data_list: list = None):  # 皓程
    from gameApp.models import Game, GamePlatform, Classification, GameType, GamePlatformRelation, GameTypeRelation
    with lock:
        if not data_list:
            return
        for game in data_list:
            obj = Game.objects.filter(name = game["game_name"],url_address = game["web_address"])
            if obj.exists():
                data_list.remove(game)
        if not data_list:
            return

        platform, _ = GamePlatform.objects.get_or_create(
            name=data_list[0]["platform"][0], loge_picture=data_list[0]["platform_logo_path"])
        game_classification_limit, _ = Classification.objects.get_or_create(
            class_name=1)
        game_classification_commen, _ = Classification.objects.get_or_create(
            class_name=0)

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


def megagames(lock):
    from gameApp.crawler.megagames import Crawl_megagames
    results = Crawl_megagames()
    save_to_database(lock,results)


def oceanofGames(lock):
    from gameApp.crawler.Ocean import OceanOfGames
    results = OceanOfGames()
    save_to_database(lock,results)


def SteamGames(lock):
    from .crawler.miyuuuu_Crawl.steam_main import Crawl_Steam

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
        save_to_database(lock,results)


def epicgames(lock):
    from gameApp.crawler.Epic import crawl_epicgames
    results = crawl_epicgames(500)
    save_to_database(lock, results)


def battlenetgames(lock):
    from gameApp.crawler.battlenet import get_battle
    results = get_battle()
    save_to_database(lock, results)



class Crawlfactory: #皓程
    def __init__(self, num_threads : int): 
        self.num_threads = num_threads
        self.tasks = queue.Queue()
        self.threads = []
        self.lock =threading.Lock()

    def add_tasks(self, task_list : list):
        for task in task_list:
            self.tasks.put(task)

    def worker(self): 
        while not self.tasks.empty():
            task = self.tasks.get()
            if task is None:
                break
            task(self.lock)
            self.tasks.task_done()

    def start_processing(self):
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker)  
            self.threads.append(thread)
            thread.start()
        for thread in self.threads:
            thread.join()


@shared_task
def work_chain():
    tasks = Crawlfactory(3)
    tasks.add_tasks([SteamGames, oceanofGames, epicgames, megagames, battlenetgames])
    tasks.start_processing()

