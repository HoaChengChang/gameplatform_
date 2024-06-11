from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from gameApp.models import Game,GamePlatform,Classification,GameType,GamePlatformRelation,GameTypeRelation
from django.core.cache import cache

@receiver(pre_delete, sender = Game)#皓程
#當Game更新前，先刪除GamePlatformRelation、GameTypeRelation,因為有foreignkey,manytomany關係
def delete_related_relations(sender, instance, **kwargs):
    GamePlatformRelation.objects.filter(game=instance).delete()
    GameTypeRelation.objects.filter(game=instance).delete()

@receiver(post_save, sender = Game)#皓程
#當Game資料庫有更新，運用signal自動更新cache
def refesh_game_cache(sender):
    cache.delete("latest_game")
    latest_objs = Game.objects.all().order_by('-release_date')[:16]
    cache.set("latest_game", latest_objs)
    gametypes = GameType.objects.all()
    for gametype in gametypes:#當cache相對應的key有值，就先刪除，再創新的資料
        cache_old = cache.get(f"{gametype.typename}_treadsgames")
        all_objs = Game.objects.filter(game_type = gametype)
        if cache_old:
            cache.delete(f"{gametype.typename}_treadsgames")
        cache.set(f"{gametype.typename}_treadsgames", all_objs)

@receiver(post_save, sender = GameType)#皓程
#當GameType資料庫有更新，運用signal自動更新cache
def refesh_game_cache(sender):
    cache.delete("all_type")
    all_objs = GameType.objects.all()
    cache.set("all_type", all_objs)
