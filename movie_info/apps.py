from django.apps import AppConfig


class MovieInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_info'
    def ready(self):
        # Import signals here to register them
        import movie_info.signals