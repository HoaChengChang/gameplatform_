# Generated by Django 4.2.2 on 2024-05-30 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameApp', '0002_remove_user_emailvalid_user_emailverify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='emailverify',
            field=models.CharField(default=None, max_length=6, null=True, verbose_name='email驗證狀態'),
        ),
    ]
