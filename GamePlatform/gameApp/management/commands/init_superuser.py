from django.conf import settings
from django.core.management.base import BaseCommand
from gameApp.models import User


class Command(BaseCommand): #皓程
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                print(user[0],user[1],user[2])
                username = user[0].replace(' ', '')
                email = user[1].replace(' ', '')
                admin = User.objects.create(email=email, username=username)
                admin.set_password(user[2].replace(' ', ''))
                admin.is_active = True
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                print(f'Creating superuser for {username} ({email})')
        else:
            print('Admin accounts can only be initialized if no User exist')
        
       
