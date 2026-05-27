from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create a demo analyst user and print an authentication token.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'demo_analyst'
        password = 'demo1234'
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f'Created user {username}')
        token, _ = Token.objects.get_or_create(user=user)
        self.stdout.write(f'API token: {token.key}')
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
