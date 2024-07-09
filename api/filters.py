import django_filters
from .models import Task, Log


class TaskFilter(django_filters.FilterSet):
    fTask_id= django_filters.NumberFilter(field_name='id')
    fTask_name = django_filters.CharFilter(field_name='task_name', lookup_expr='icontains')
    fTask_desctiption = django_filters.CharFilter(field_name='task_description', lookup_expr='icontains')
    # fTask_staus = django_filters.NumberFilter(field_name='task_status', choices=Task.STATUS)
    fTask_staus = django_filters.NumberFilter(field_name='task_status')
    fTask_user = django_filters.NumberFilter(field_name='task_user')

    class Meta:
        model = Task
        fields = [
            'fTask_id',
            'fTask_name',
            'fTask_desctiption',
            'fTask_staus',
            'fTask_user'
        ]


class LogFilter(django_filters.FilterSet):
    fTask_id = django_filters.NumberFilter(field_name='task_id')

    class Meta:
        model = Log
        fields = [
            'fTask_id',
        ]
