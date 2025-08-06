from django.apps import AppConfig

class AnalyticsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics_app'
    
    def ready(self):
        # Place for startup code (optional)
        pass