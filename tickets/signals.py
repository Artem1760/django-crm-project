from django.db.models.signals import pre_save
from django.dispatch import receiver

from tickets.models import Category, Ticket


@receiver(pre_save, sender=Ticket)
def pre_save_ticket(sender, instance, **kwargs):
    """
    Signal to automatically set the category to 'assigned' when a new
    associate is selected.
    """
    if instance.associate and not instance.category:
        instance.category = Category.objects.get(name='assigned')


@receiver(pre_save, sender=Ticket)
def pre_save_ticket_unset_category(sender, instance, **kwargs):
    """
    Signal to automatically unset the category when the associate is set to None.
    """
    if instance.associate is None:
        instance.category = None
