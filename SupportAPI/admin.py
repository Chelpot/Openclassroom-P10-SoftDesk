from django.contrib import admin
from .models import Project, Contributor, Issue, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'author')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag', 'project')