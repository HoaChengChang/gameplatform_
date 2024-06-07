from django.core.cache import cache
from .models import User,GamePlatform,GameType,Classification,Game,GamePlatformRelation,GameTypeRelation,Comment,CommentArea,CommentAreaReview
from django.shortcuts import get_object_or_404

def get_redis_cache(target : str = None,key = None):#皓程
    if target == None or key == None:
        return None
    
    match target:# match func is for python 3.10 up
        case "all_type_games":# key:type_obj
            all_objs = cache.get(f"{key.typename}_treadsgames")
            if all_objs is None:
                # 如果缓存中没有找到，查詢資料庫
                all_objs = Game.objects.filter(game_type = key)
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(f"{key.typename}_treadsgames", all_objs)
            return all_objs
        case "latest_game": 
            all_objs = cache.get(key)
            if all_objs is None:
                # 如果缓存中没有找到，查詢資料庫
                all_objs = Game.objects.all().order_by('-release_date')[:16]
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(key, all_objs)
            return all_objs
        case "game_type":# key:type_str
            obj = cache.get(key)
            if obj is None:
                # 如果缓存中没有找到，查詢資料庫
                obj = GameType.objects.get(typename = key)
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(key, obj)
            return obj
        case "game":# key:"id_int"
            key_str = target+str(key)
            game_obj = cache.get(key_str)
            if game_obj is None:
                # 如果缓存中没有找到，查詢資料庫
                game_obj = get_object_or_404(Game, id = key)
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(key_str, game_obj)
            return game_obj
        case "user":# key:"username_str"
            user_obj = cache.get(key)
            if user_obj is None:
                # 如果缓存中没有找到，查詢資料庫
                user_obj = get_object_or_404(User, username = key)
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(key, user_obj)
            return user_obj
        case "all_type_objs":# key:"all_type"
            all_objs = cache.get(key)
            if all_objs is None:
                # 如果缓存中没有找到，查詢資料庫
                all_objs = GameType.objects.all()
                # 將查詢结果存在缓存中，以便下次使用
                cache.set(key, all_objs)
            return all_objs



    