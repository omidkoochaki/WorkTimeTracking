from django.urls import path
from rest_framework import routers

from .views import ProjectAPIView, TaskAPIView, WorkingTimeAPIViewCreate, WorkingTimeAPIViewStop, InviteMembersView, \
        ResponseToInvitation

router = routers.DefaultRouter()
router.register('projects', ProjectAPIView, 'projects')
router.register('tasks', TaskAPIView, 'tasks')

urls = [path('stop', WorkingTimeAPIViewStop.as_view(), name='working_time_stop'),
        path('start', WorkingTimeAPIViewCreate.as_view(), name='working_time_start'),
        path('invite_members', InviteMembersView.as_view(), name='invite_members'),
        path('invitation_response', ResponseToInvitation.as_view(), name='invitation_response')
        ]
urlpatterns = router.urls + urls
