from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task, Log
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(pre_save, sender=Task)
def log_task_changes(
    sender, 
    instance, 
    **kwargs):
    if instance.pk:
        pre_instance = Task.objects.get(pk=instance.pk)

        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(
                pre_instance, 
                field_name)
            new_value = getattr(
                instance, 
                field_name)

            if old_value != new_value:
                Log.objects.create(
                    task_field_name=field_name,
                    prev_value=old_value,
                    new_value=new_value,
                    task_id=instance
                )


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
        Token.objects.create(user = instance)
