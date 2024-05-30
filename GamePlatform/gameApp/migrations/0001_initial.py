# Generated by Django 4.2.2 on 2024-05-27 14:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gameApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(default=None, max_length=11, null=True, verbose_name='手機號碼')),
                ('gender', models.IntegerField(choices=[[0, '男'], [1, '女']], default=0, verbose_name='性別')),
                ('icon', models.ImageField(default='media/icon/default.jpg', upload_to=gameApp.models.icon_rename, verbose_name='頭貼')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('emailValid', models.IntegerField(default=0, verbose_name='email驗證狀態')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='gameapp_user_set', related_query_name='user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='gameapp_user_set', related_query_name='user', to='auth.permission')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.IntegerField(choices=[[0, '普遍級'], [1, '限制級']], default=0)),
            ],
            options={
                'verbose_name': '分級',
                'verbose_name_plural': '分級',
                'db_table': 'classification',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('star_count', models.FloatField()),
                ('dt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '評論區',
                'verbose_name_plural': '評論區',
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('introduction', models.TextField()),
                ('hardware_or_fileinfo', models.TextField()),
                ('release_date', models.DateField()),
                ('pay', models.BooleanField(default=True)),
                ('picture_game', models.CharField(max_length=250)),
                ('url_address', models.CharField(max_length=250)),
                ('game_type_tmp', models.CharField(max_length=50)),
                ('game_classification', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='gameApp.classification')),
            ],
            options={
                'verbose_name': '遊戲',
                'verbose_name_plural': '遊戲',
                'db_table': 'Game',
            },
        ),
        migrations.CreateModel(
            name='GamePlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('loge_picture', models.TextField()),
                ('introduction', models.TextField()),
            ],
            options={
                'verbose_name': '發布平台',
                'verbose_name_plural': '發布平台',
                'db_table': 'GamePlatform',
            },
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.CharField(default='免費', max_length=25)),
            ],
            options={
                'verbose_name': '種類',
                'verbose_name_plural': '種類',
                'db_table': 'GameType',
            },
        ),
        migrations.CreateModel(
            name='GameTypeRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gameApp.game')),
                ('game_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameApp.gametype')),
            ],
        ),
        migrations.CreateModel(
            name='GamePlatformRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gameApp.game')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameApp.gameplatform')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.ManyToManyField(related_name='games', through='gameApp.GameTypeRelation', to='gameApp.gametype'),
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.ManyToManyField(related_name='games', through='gameApp.GamePlatformRelation', to='gameApp.gameplatform'),
        ),
        migrations.CreateModel(
            name='CommentUserRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gameApp.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='game',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='gameApp.game'),
        ),
        migrations.AddField(
            model_name='comment',
            name='game_like',
            field=models.ManyToManyField(related_name='like', through='gameApp.CommentUserRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
