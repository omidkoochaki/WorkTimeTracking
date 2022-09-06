from django.urls import path
from rest_framework import routers

from .views import ProjectAPIView, TaskAPIView, WorkingTimeAPIViewCreate, WorkingTimeAPIViewStop, InviteMembersView, \
        ResponseToInvitation

router = routers.DefaultRouter()
router.register('projects', ProjectAPIView, 'projects')
router.register('tasks', TaskAPIView, 'tasks')
# router.register('invitation_response', ResponseToInvitation, 'invitation_response')
# router.register('times', WorkingTimeAPIViewCreate.as_view(), 'working_time_records')
# router.register('stop', WorkingTimeAPIViewStop.as_view(), 'working_time_records')
# urls = [path('times/', WorkingTimeAPIView.as_view(
#             {
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             }
#         ), name="working_time_records"),
#
#         path('projects/', ProjectAPIView.as_view(
#             {
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             }
#         ), name="projects"),
#
#         ]

urls = [path('stop', WorkingTimeAPIViewStop.as_view(), name='working_time_stop'),
        path('start', WorkingTimeAPIViewCreate.as_view(), name='working_time_start'),
        path('invite_members', InviteMembersView.as_view(), name='invite_members'),
        path('invitation_response', ResponseToInvitation.as_view(), name='invitation_response')
        ]
urlpatterns = router.urls + urls
# urlpatterns = router.urls
# 844022
# 4