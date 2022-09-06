from rest_framework import serializers
from time_tracker.models import Project, Task, WorkTimeRecord, InvitedMembers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class WorkTimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTimeRecord
        fields = '__all__'


class WorkTimeRecordSerializerStart(serializers.ModelSerializer):
    class Meta:
        model = WorkTimeRecord
        fields = ['project', 'task']


class InviteMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedMembers
        # TODO: Remove 'invitation_code' field in production
        fields = ['email', 'project', 'invitation_code']


class ResponseToInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedMembers
        fields = ['email', 'invitation_code']

