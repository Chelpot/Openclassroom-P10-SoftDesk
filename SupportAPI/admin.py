from django.contrib import admin
from .models import Project, Contributor, Issue, User, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'project')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type', 'author')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','flag', 'project')\

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content','created_time', 'id', 'author', 'issue')