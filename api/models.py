from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    STATUS = [
        (0, 'Nowy'),
        (1, "W toku"),
        (2, "Rozwiązany")
    ]

    task_name = models.CharField(max_length=124, blank=False, null=False)
    task_description = models.TextField(default='', blank=None, null=None)
    task_status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    task_user = models.ForeignKey(User, 
                                  on_delete=models.CASCADE, 
                                  blank=True, null=True)

    def __str__(self):
        return "{}".format(self.task_name)


class Log(models.Model):
    task_field_name = models.CharField(max_length=32, null=False, blank=False)
    prev_value = models.TextField(default='', null=True, blank=True)
    new_value = models.TextField(default='', null=True, blank=True)
    change_time = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE,
                                blank=False, null=False)
    
    def __str__(self) -> str:
        return "{} -> {}".format(self.task_id, self.task_field_name)

