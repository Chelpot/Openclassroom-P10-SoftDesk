from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, ProjectViewSet
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('', include(router.urls))
]
