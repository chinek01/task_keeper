from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets, filters
from .serializers import (
    TaskSerializer,
    LogSerializer,
    UserSerializer
)
from .models import (
    Task,
    Log
)


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    filter_fields = (
        'task_name',
        'task_description',
        'task_status',
        'task_user'
    )
    search_fields = (
        'task_name',
        'task_description',
    )

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset;


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = TaskSerializer(queryset, many=True)

        fTask_name = request.query_params.get('task_name', None)

        tasks = Task.objects.filter(task_name__icontains = fTask_name)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        
        # TODO: on authenticated user 
        user = None
        if request.user.id:
            user = User.objects.filter(id=request.user.id)  

        new_task = Task.objects.create(
            task_name = request.data['task_name'],
            task_description = request.data['task_description'],
            task_status = 1,
            task_user = user,
        )

        serializer = TaskSerializer(new_task, many=False)
        
        return Response(serializer.data)
        
        # return super().create(request, *args, **kwargs)
    

    def get_queryset(self):
        # return super().get_queryset()
        # TODO: on authenticated user 

        tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)

        # return Response(serializer.data)
        return tasks


    # def update(self, request, *args, **kwargs):

    #     # # TODO: on authenticated user 
    #     # update_task = self.get_object()

    #     # # TODO: dodanie obiektu log i jego uzupełnienie
        
    #     # update_task.task_name = request.data['task_name']
    #     # update_task.task_description = request.data['task_description']
    #     # update_task.task_status = request.data['task_status']
        
    #     # # TODO: task user 
    #     # #update_task.task_user = request.data['task_user']

    #     # update_task.save()

    #     # serializer = TaskSerializer(update_task, many=False)
    #     # return Response(serializer.data)
    

    def destroy(self, request, *args, **kwargs):

        # TODO: on authenticated user 
        task = self.get_object()
        task.delete()

        return Response("Task deleted")
        # return super().destroy(request, *args, **kwargs)
    

        # return super().update(request, *args, **kwargs)

