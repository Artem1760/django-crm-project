import os

from django.db import models
from django.urls import reverse

from associates.models import Associate, UserDepartment


class TicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


TICKET_TYPES = (
    (1, 'Type 1'),
    (2, 'Type 2'),
    (3, 'Type 3')
)

CATEGORIES = (
    ('assigned', 'Assigned'),
    ('work_in_progress', 'Work in Progress'),
    ('processed', 'Processed'),
    ('completed', 'Completed'),
    ('returned', 'Returned')
)


def ticket_upload_files(instance, filename):
    """Generates the file path for ticket files based on ticket ID."""
    return os.path.join('ticket_files', f'ticket_{instance.id}', filename)


class Ticket(models.Model):
    title = models.CharField(max_length=150)
    type = models.IntegerField(choices=TICKET_TYPES)
    description = models.TextField(default='Describe your task here.')
    uploaded_file = models.FileField(null=True, blank=True,
                                     upload_to=ticket_upload_files)
    uploaded_image = models.ImageField(null=True, blank=True,
                                       upload_to=ticket_upload_files)
    created_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)
    associate = models.ForeignKey(Associate, on_delete=models.SET_NULL,
                                  related_name='associates', null=True,
                                  blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 related_name='categories', null=True,
                                 blank=True)

    objects = TicketManager()

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ('-created_date',)

    def __str__(self):
        return f'{self.title}, id: {self.pk}'

    def get_absolute_url(self):
        return reverse('tickets:ticket-detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=30, choices=CATEGORIES, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('id',)

    def __str__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse('tickets:category-detail', kwargs={'pk': self.pk})


def upload_follow_ups(instance, filename):
    return f'ticket_files/ticket_{instance.ticket.id}/ticket_followups/{filename}'


class FollowUp(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='followups',
                               on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=upload_follow_ups)

    class Meta:
        verbose_name = 'FollowUp'
        verbose_name_plural = 'FollowUps'
        ordering = ('-created_date',)

    def __str__(self):
        return f'Ticket id: {self.ticket.id} FollowUp'
