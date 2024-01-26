from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_associate = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.get_full_name()


class UserDepartment(models.Model):
    """ Model to store the organizer information for associates.  """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username.title()


class Associate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('UserDepartment', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Associate'
        verbose_name_plural = 'Associates'
        ordering = ('id',)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('associates:associate-detail', kwargs={'pk': self.pk})
