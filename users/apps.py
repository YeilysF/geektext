from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(selft):
        import users.signals