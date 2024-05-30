from django.db.models.signals import pre_delete
from django.dispatch import receiver
from gameApp.models import Game,GamePlatform,Classification,GameType,GamePlatformRelation,GameTypeRelation


@receiver(pre_delete, sender = Game)
def delete_related_relations(sender, instance, **kwargs):
    GamePlatformRelation.objects.filter(game=instance).delete()
    GameTypeRelation.objects.filter(game=instance).delete()