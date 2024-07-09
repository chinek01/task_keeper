from django.urls import include, path
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'task', viewset=views.TaskViewSet)
router.register(r'log', viewset=views.LogViewSet)
router.register(r'user', viewset=views.UserViewSet)


urlpatterns = [
    path('', include(router.urls))
]
