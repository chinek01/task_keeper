from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import (
    Task,
    Log
)

# some serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
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

    def create(self, validated_data):
        """
        overwritten user creation function, automatically add user group
        """
        user = User.objects.create_user(**validated_data)

        # add user group 
        group = Group.objects.get(name='api_users')
        user.groups.add(group)
        return user


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
        read_only_fields = [
            'id', 
            'task_user']


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
        read_only_fields = [ 
            'id', 
            'change_time', 
            'task_id' ]
