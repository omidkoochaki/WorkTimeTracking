import enum


class TagNames(enum.Enum):
    PROJECTS_TAG_NAME = "Projects"
    TASKS_TAG_NAME = "Tasks"
    # _TAG_NAME = "Tasks"


class ResponseCodes(enum.Enum):
    CODES = {
        401: 'Unauthorised',
        201: 'Created',
        404: 'unauthorized',
    }
