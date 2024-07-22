import django_filters
from .models import Task, Log


class TaskFilter(django_filters.FilterSet):
    task_id= django_filters.NumberFilter(field_name='id')
    task_name = django_filters.CharFilter(field_name='task_name', lookup_expr='icontains')
    task_desctiption = django_filters.CharFilter(field_name='task_description', lookup_expr='icontains')
    task_staus = django_filters.NumberFilter(field_name='task_status')
    task_user = django_filters.NumberFilter(field_name='task_user')

    class Meta:
        model = Task
        fields = [
            'task_name',
            'task_desctiption',
            'task_staus',
            'task_user'
        ]


class LogFilter(django_filters.FilterSet):
    task_id = django_filters.NumberFilter(field_name='task_id')

    class Meta:
        model = Log
        fields = [
            'task_id',
        ]
