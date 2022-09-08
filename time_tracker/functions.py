import datetime

from time_tracker.models import InvitedMembers, Project, WorkTimeRecord, TaskDailyReporting


def invitation_code_validator(email, code) -> int | Project:
    try:
        member = InvitedMembers.objects.get(email=email, invitation_code=code)
    except:
        member = None
    if member:
        return member.project
    else:
        return -1


def calculate_task_total_time_in_day():
    all_records_last_day = list(WorkTimeRecord.objects.filter(year=datetime.datetime.now().year,
                                  month=datetime.datetime.now().month,
                                  day=(datetime.datetime.now().day-1)))
    all_tasks_worked_on_last_day = {}
    for wtr in all_records_last_day:
        if wtr.task.id not in all_tasks_worked_on_last_day.keys():
            all_tasks_worked_on_last_day[wtr.task.id] = wtr.duration
            print(wtr.duration, '*#'*10)
        else:
            all_tasks_worked_on_last_day[wtr.task.id] = all_tasks_worked_on_last_day[wtr.task.id] + wtr.duration
    for task_id in all_tasks_worked_on_last_day.keys():
        try:
            obj = TaskDailyReporting.objects.get(task__id=task_id)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except Person.DoesNotExist:
            new_values = {'first_name': 'John', 'last_name': 'Lennon'}
            new_values.update(defaults)
            obj = Person(**new_values)
            obj.save()
    return all_tasks_worked_on_last_day


def calculate_project_total_time_in_day():
    return []

