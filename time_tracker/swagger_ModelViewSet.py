from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets


class SwaggerDescription:
    def __init__(self, operation_description: str, tags: list, operation_summary: str, responses: dict):
        self.operation_description = operation_description
        self.tags = tags
        self.operation_summary = operation_summary
        self.responses = responses


class SwaggerModelViewSet(viewsets.ModelViewSet):

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
