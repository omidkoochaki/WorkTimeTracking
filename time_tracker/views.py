import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from time_tracker.permissions import IsMemberInProject, IsProjectOwner
from time_tracker.models import Project, Task, WorkTimeRecord, InvitedMembers
from .functions import invitation_code_validator
from .serializers import ProjectSerializer, TaskSerializer, WorkTimeRecordSerializer, WorkTimeRecordSerializerStart, \
    InviteMemberSerializer, ResponseToInvitationSerializer


class ProjectAPIView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @swagger_auto_schema(operation_description="This method will return a list of projects owned by the user",
                         tags=['Projects'], operation_summary="Returns list of User's projects", )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will create a project owned by the user",
                         tags=['Projects'], operation_summary="Creates a project owned by user",
                         responses={'404': 'unauthorized'})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will return a project owned by the user by its id",
                         tags=['Projects'], operation_summary="Get a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will delete a project owned by the user by its id",
                         tags=['Projects'], operation_summary="remove a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will update a project owned by the user by its id",
                         tags=['Projects'], operation_summary="update a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskAPIView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @swagger_auto_schema(operation_description="This method will return a list of projects owned by the user",
                         tags=['Tasks'], operation_summary="Returns list of User's projects", )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will create a project owned by the user",
                         tags=['Tasks'], operation_summary="Creates a project owned by user",
                         responses={'404': 'unauthorized'})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will return a project owned by the user by its id",
                         tags=['Tasks'], operation_summary="Get a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will delete a project owned by the user by its id",
                         tags=['Tasks'], operation_summary="remove a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="This method will update a project owned by the user by its id",
                         tags=['Tasks'], operation_summary="update a project owned by user by its id",
                         responses={'404': 'unauthorized'})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(assignee=self.request.user)


class WorkingTimeAPIViewCreate(generics.CreateAPIView):
    serializer_class = WorkTimeRecordSerializerStart
    permission_classes = [
        permissions.IsAuthenticated,
        IsMemberInProject
    ]

    def perform_create(self, serializer):
        if self.request.user in Project.objects.get(id=self.request.data.get('project')):
            serializer.save(doer=self.request.user)
        else:
            raise Exception("You should be a member in this project")

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def get_object(self):
    #     return WorkTimeRecord.objects.all()

    # def get_queryset(self):
    #     # return self.request.user.leads.all()
    #     return WorkTimeRecord.objects.all()
    #
    # def perform_create(self, serializer):
    #     serializer.save()


class WorkingTimeAPIViewStop(APIView):
    serializer_class = WorkTimeRecordSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def put(self, request):
        print(request)
        return Response({'yes': 'yes'})

    def get(self, request):
        print(request)
        return Response({'yes': 'yes'})


class InviteMembersView(generics.CreateAPIView):
    serializer_class = InviteMemberSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsProjectOwner
    ]

    def perform_create(self, serializer):
        # if self.request.user in Project.objects.get(id=self.request.data.get('project')):
        invitation_code = random.randint(100000, 999999)
        # TODO: Send Invitation Email - celery task
        serializer.save(invitation_code=invitation_code)


class ResponseToInvitation(APIView):
    serializer_class = ResponseToInvitationSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    # def get_queryset(self):
    #     code = self.request.data.get('invitation_code')
    #     email = self.request.data.get('email')
    #     validate = invitation_code_validator(email, code)
    #     if validate != -1:
    #         return Project.objects.get(id=validate)

    def put(self, request, *args, **kwargs):
        code = self.request.data.get('invitation_code')
        email = self.request.user.email
        prj = invitation_code_validator(email, code)
        if prj != -1:
            # prj = Project.objects.get(id=validate)
            # prj.members.add(self.request.user)
            prj.members.add(self.request.user)
            return Response({"msg": f"welcome to {prj.title}"})
        else:
            raise Exception("You are not invited")

    # def perform_update(self, serializer):
    #     pass
