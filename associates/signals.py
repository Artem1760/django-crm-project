from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from associates.models import UserDepartment

User = get_user_model()


@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    """
    Signal handler to create a UserDepartment instance when a new 
    organizer user is created.
    """
    if created and instance.is_organizer:
        UserDepartment.objects.get_or_create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
