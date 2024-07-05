from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Task,
    Log
)

# some serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'id', 'username', 'email', 'groups']
        # rozszerzone o zakładanie nowego usera
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True
            }
        }



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [ 
            'id',
            'task_name',
            'task_description',
            'task_status',
            'task_user'
        ]
        read_only_fields = ['id', 'task_user']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = [
            'id',
            'task_field_name',
            'prev_value',
            'new_value',
            'change_time',
            'task_id'
        ]
        read_only_fields = [ 'id', 'change_time', 'task_id' ]
