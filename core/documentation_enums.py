import enum


class TagNames(enum.Enum):
    PROJECTS_TAG_NAME = "Projects"
    TASKS_TAG_NAME = "Tasks"
    INVITE_MEMBERS = "Invite Members"


class ResponseCodes(enum.Enum):
    CODES = {
        401: 'Unauthorised',
        201: 'Created',
        404: 'unauthorized',
    }
