from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your models here.

@receiver(post_save, sender=User)
def create_auth_token(
        sender,
        instance=None,
        created=False,
        **kwargs
):
    """
    Tylko w momencie utworzenia użytkownika ma zostać stworzony token
    """
    if created:
        Token.objects.create(user=instance)


class Task(models.Model):
    STATUS = [
        (0, 'Nowy'),
        (1, "W toku"),
        (2, "Rozwiązany")
    ]

    task_name = models.CharField(max_length=124, blank=False, null=False)
    task_description = models.TextField(default='', blank=None, null=None)
    task_status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    task_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.task_name)


class Log(models.Model):
    task_field_name = models.CharField(max_length=32, null=False, blank=False)
    prev_value = models.TextField(default='', null=True, blank=True)
    new_value = models.TextField(default='', null=True, blank=True)
    change_time = models.DateTimeField(auto_now_add=True)
    task_id = models.PositiveIntegerField(null=False, blank=False)
