from time_tracker.models import InvitedMembers, Project


def invitation_code_validator(email, code) -> int | Project:
    member = InvitedMembers.objects.get(email=email, invitation_code=code)
    if member:
        print(member.project)
        print('-_' * 40)
        print(type(member.project))
        return member.project
    else:
        return -1
