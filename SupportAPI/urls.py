from django.urls import path
from .views import CreateUserView, ProjectCreateView

urlpatterns = [
    path('users/', CreateUserView.as_view(), name='user-create'),
    path('projects/', ProjectCreateView.as_view(), name='project-create'),
]
