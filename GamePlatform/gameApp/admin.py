from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,GamePlatform,GameType,Classification,Game,GamePlatformRelation,GameTypeRelation


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_login', 'is_superuser', 'email','is_staff' ,'is_active','date_joined','phone','gender','icon')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone','gender','icon')}),  # 确保这些字段在用户详情页面中显示
    )
    model = User

class GamePlatformRelationInline(admin.TabularInline):
    model = GamePlatformRelation
    extra = 1  # 可选：默认提供一个额外空白行

class GameTypeRelationInline(admin.TabularInline):
    model = GameTypeRelation
    extra = 1  # 可选：默认提供一个额外空白行

@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = ('name','introduction','hardware_or_fileinfo','game_classification','release_date','pay','picture_game','url_address')
    fieldsets = (
        (None, {
            'fields': ('name', 'introduction', 'hardware_or_fileinfo', 'game_classification', 'deploy_time', 'pay', 'picture_game', 'url_address')
        }),
    )
    inlines = [GamePlatformRelationInline, GameTypeRelationInline]
    model = Game
@admin.register(GameType)
class GameType_(admin.ModelAdmin):
    list_display = ('typename',)
    # fieldsets = (
    #     (None, {'fields': ('typename')}),  # 确保这些字段在用户详情页面中显示
    # )
    model = GameType

@admin.register(Classification)
class Classification_(admin.ModelAdmin):
    list_display = ('class_name',)
    # fieldsets = (
    #     (None, {'fields': ('class_name')}),  # 确保这些字段在用户详情页面中显示
    # )
    model = Classification

@admin.register(GamePlatform)
class GamePlatform_(admin.ModelAdmin):
    list_display = ('name', 'loge_picture', 'introduction')
    # fieldsets = (
    #     (None, {'fields': ('name')}),  # 确保这些字段在用户详情页面中显示
    # )
    model = GamePlatform