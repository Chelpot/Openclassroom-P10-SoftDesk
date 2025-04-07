from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import CreateUserView, ProjectViewSet, IssueViewSet, CommentViewSet

#Main router
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

#Second level router for issues in projects
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

#Third level router for comments in issues
issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]
