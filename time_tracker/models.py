import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

# Create your models here.
from rest_framework.exceptions import MethodNotAllowed, NotAcceptable

from core.BaseModels import BaseModel, BaseManager


class Project(BaseModel):
    """
    stores a project with its name,
    :param title:
        Project Title:
    :param budget:
        Project Budget
    """
    title = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, related_name="owner_of_projects", null=True, on_delete=CASCADE)
    budget = models.FloatField(default=0)
    deadline = models.DateField(default=datetime.date.today() + datetime.timedelta(days=5))
    members = models.ManyToManyField(User, related_name='member_in_projects', blank=True)


class Task(BaseModel):
    """
    each task is related to one project.
    assignee is responsible for delivering the task.
    acceptance_criteria is a note for the owner to
    confirm the task is done and a description for
    assignee to know what should be delivered.
    """
    project = models.ForeignKey(Project, related_name='tasks', on_delete=CASCADE)
    title = models.CharField(max_length=100)
    assignee = models.ForeignKey(User, related_name='assignee_in_tasks', on_delete=PROTECT, default=None)
    acceptance_criteria = models.TextField(default=None)

    class Meta:
        unique_together = ('project', 'title')


class WorkTimeRecord(BaseModel):
    """
    each task can get done in different times.
    """
    project = models.ForeignKey(Project, related_name='task_time_record', on_delete=CASCADE)
    task = models.ForeignKey(Task, related_name='time_record', on_delete=CASCADE)
    doer = models.ForeignKey(User, on_delete=PROTECT, default=None)
    start_time = models.FloatField(default=datetime.datetime.now().timestamp())
    end_time = models.FloatField(blank=True, null=True)
    year = models.IntegerField(default=datetime.datetime.now().year)
    month = models.IntegerField(default=datetime.datetime.now().month)
    day = models.IntegerField(default=datetime.datetime.now().day)

    objects = BaseManager()

    @property
    def duration(self):
        if self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return 0
            # raise NotAcceptable(detail='First hit the Stop working then ask for duration')

    class Meta:
        unique_together = ('task', 'year', 'month', 'day', 'doer', 'end_time')
        #  with make end_time unique with doer we guarantee that each doer will start a task once before end it.


class InvitedMembers(BaseModel):
    project = models.ForeignKey(Project, on_delete=CASCADE)
    invitation_code = models.CharField(max_length=9)
    email = models.EmailField()

    class Meta:
        unique_together = ('email', 'project')


class TaskDailyReporting(BaseModel):
    """
    at 1 AM a celery worker will do the calculations
    """
    task = models.ForeignKey(Task, on_delete=CASCADE, unique=True)
    total_time_seconds = models.IntegerField(default=0)
    year = models.IntegerField(default=datetime.datetime.now().year)
    month = models.IntegerField(default=datetime.datetime.now().month)
    day = models.IntegerField(default=datetime.datetime.now().day)


class ProjectDailyReporting(BaseModel):
    """
    at 1 AM a celery worker will do the calculations
    """
    project = models.ForeignKey(Project, on_delete=CASCADE, unique=True)
    total_time_seconds = models.IntegerField(default=0)
    year = models.IntegerField(default=datetime.datetime.now().year)
    month = models.IntegerField(default=datetime.datetime.now().month)
    day = models.IntegerField(default=datetime.datetime.now().day)
