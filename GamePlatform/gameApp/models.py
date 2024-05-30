from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
import os
#資料庫設計：皓程
def icon_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('media/icon', filename)

# Create your models here.
class User(AbstractUser):
    SEX_CHOICES = [
        [0, '男'],
        [1, '女'],
    ]
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='gameapp_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='gameapp_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
    phone = models.CharField(max_length=11, null=True, default=None, verbose_name="手機號碼")
    gender = models.IntegerField(choices=SEX_CHOICES, default=0, verbose_name="性別")
    icon = models.ImageField(upload_to=icon_rename, default="media/icon/default.jpg", verbose_name="頭貼")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    emailverify = models.CharField(max_length=6, default="0", verbose_name="email驗證狀態")

    class Meta:
        db_table='user'
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username
    

class GameType(models.Model):
    typename = models.CharField(max_length=25,null=False,default='免費')

    class Meta:
        db_table='GameType'
        verbose_name='種類'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '%s' %self.typename

LEVEL_CHOICES = [
        [0,'普遍級'],
        [1,'限制級'],
    ]
class Classification(models.Model):
    class_name = models.IntegerField(choices=LEVEL_CHOICES,default=0)
    
    class Meta:
        db_table='classification'
        verbose_name='分級'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '%s' %self.class_name
    

class GamePlatform(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    loge_picture = models.TextField() #ImageField(upload_to = "GamePlatform_logo" ,default="logo/default.jpg")
    introduction = models.TextField()
    
    class Meta:
        db_table='GamePlatform'
        verbose_name='發布平台'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '%s' %self.name
    

class Game(models.Model): 
    name = models.CharField(max_length=200,null=False,blank=False)
    introduction = models.TextField()
    hardware_or_fileinfo = models.TextField()
    platform = models.ManyToManyField(
        to='GamePlatform',  
        through='GamePlatformRelation',  
        related_name='games',   
    )
    game_type = models.ManyToManyField(
        to='GameType',  
        through='GameTypeRelation',  
        related_name='games',  
    )
    game_classification = models.ForeignKey(
        to='Classification',  
        db_constraint=False,  
        related_name='games',
        null = True,
        on_delete=models.SET_NULL 
    )
    release_date = models.DateField() 
    pay = models.BooleanField(default=True) 
    picture_game = models.CharField(max_length=250,null=False,blank=False)
    url_address = models.CharField(max_length=250,null=False,blank=False)
    game_type_tmp = models.CharField(max_length=50,null=False,blank=False)
    
    @property
    def get_classification_display(self):
        return dict(LEVEL_CHOICES).get(self.game_classification.class_name, 'Unknown')
    
    class Meta:
        db_table='Game'
        verbose_name='遊戲'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '%s' %self.name

class Comment(models.Model):
    game = models.ForeignKey(
        to='Game',  
        db_constraint=False,  
        related_name='comments',  
        null = True,
        on_delete=models.SET_NULL,
    )
    user = models.ForeignKey(
        to='User',  
        db_constraint=False,  
        related_name='comments',  
        on_delete=models.CASCADE,
    )
    game_like = models.ManyToManyField(
        to='User',  
        through='CommentUserRelation',  
        related_name='like',  
    )
    context = models.TextField()
    star_count = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)

    @property
    def get_commentlike_count(self):
        return self.game_like.count()

    class Meta:
        db_table='Comment'
        verbose_name='評論區'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '%s' %self.game.name

class GamePlatformRelation(models.Model):
    game = models.ForeignKey(Game, null = True, on_delete=models.SET_NULL)
    platform = models.ForeignKey(GamePlatform, on_delete=models.CASCADE)

class GameTypeRelation(models.Model):
    game = models.ForeignKey(Game, null = True, on_delete=models.SET_NULL)
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)

class CommentUserRelation(models.Model):
    comment = models.ForeignKey(Comment, null = True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

