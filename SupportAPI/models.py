from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Project(models.Model):
    BACK = 'back-end'
    FRONT = 'front-end'
    ANDROID = 'Android'
    IOS = 'IOS'

    TYPE_CHOICES = (
        (BACK, 'back-end'),
        (FRONT, 'front-end'),
        (ANDROID, 'Android'),
        (IOS, 'IOS'),
    )

    type = models.CharField(max_length=30, choices=TYPE_CHOICES, verbose_name='Priorité')
    name = models.CharField(max_length=30)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owned_projects')
    description = models.TextField(verbose_name="Description")
    contributors = models.ManyToManyField(
        to='User',
        through='Contributor',
        related_name='projects'
    )

    def __str__(self):
        return f"[{self.name}] - {self.type} ----- Author : {self.author.username}"

class Contributor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    def __str__(self):
        return f"[{self.user.username}] - {self.project.name}"

class Issue(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'

    TODO = 'TODO'
    INPROGRESS = 'INPROGRESS'
    FINISHED = 'FINISHED'

    ISSUE_CHOICES = (
        (LOW, 'Faible'),
        (MEDIUM, 'Moyenne'),
        (HIGH, 'Haute'),
    )
    FLAG_CHOICES = (
        (FEATURE, 'Fonctionnalité'),
        (TASK, 'Tâche'),
        (BUG, 'Bug'),
    )
    STATUS_CHOICES = (
        (TODO, 'A faire'),
        (INPROGRESS, 'En progrès'),
        (FINISHED, 'Fini'),
    )
    name = models.CharField(max_length=100, verbose_name="Nom du problème")
    description = models.TextField(verbose_name="Description")
    flag = models.CharField(max_length=30, choices=FLAG_CHOICES, verbose_name='Balise')
    priority = models.CharField(max_length=30, choices=ISSUE_CHOICES, verbose_name='Priorité')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Status', default=TODO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='Issues')
    user_responsible = models.OneToOneField(User, on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owned_issues')

    def __str__(self):
        return f"[{self.project.name}] - {self.name}"