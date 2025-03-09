from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class User(AbstractUser):
    age = models.PositiveIntegerField(),
    can_be_contacted = models.BooleanField(default=False),
    can_data_be_shared = models.BooleanField(default=False),

    def __str__(self):
        return self.username

class Project(Model):
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
    description = models.TextField(verbose_name="Description")

    pass


class Issue(Model):
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
    priority = models.CharField(max_length=30, choices=ISSUE_CHOICES, verbose_name='Priorité')
    flag = models.CharField(max_length=30, choices=FLAG_CHOICES, verbose_name='Balise')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, verbose_name='Status', default=TODO)
    project = models.ForeignKey('SoftDesk.Project', on_delete=models.CASCADE, related_name='Issues')
    name = models.CharField(max_length=100, verbose_name="Nom du problème")
    description = models.TextField(verbose_name="Description")
    user_responsible = models.OneToOneField(User, on_delete=models.CASCADE)
