from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import CreateUserView, ProjectViewSet, IssueViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]
