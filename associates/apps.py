from django.apps import AppConfig


class AssociatesConfig(AppConfig):
    name = 'associates'
    
    def ready(self):
        
        import associates.signals
