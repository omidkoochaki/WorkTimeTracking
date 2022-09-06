from rest_framework import serializers
from time_tracker.models import Project, Task, WorkTimeRecord, InvitedMembers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'budget', 'deadline', 'owner', 'members']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class WorkTimeRecordSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(many=True, read_only=True)
    # task = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = WorkTimeRecord
        fields = ['project', 'task']


class WorkTimeRecordSerializerStart(serializers.ModelSerializer):
    # project = ProjectSerializer(many=True, read_only=True)
    # task = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = WorkTimeRecord
        fields = ['project', 'task']


class InviteMemberSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = InvitedMembers
        # TODO: Remove 'invitation_code' field in production
        fields = ['email', 'project', 'invitation_code']


class ResponseToInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedMembers
        fields = ['invitation_code']


#951142