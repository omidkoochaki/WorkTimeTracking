from datetime import datetime, timedelta

from time_tracker.models import InvitedMembers, Project, WorkTimeRecord, TaskDailyReporting, ProjectDailyReporting


def invitation_code_validator(email, code) -> int | Project:
    try:
        member = InvitedMembers.objects.get(email=email, invitation_code=code)
    except:
        member = None
    if member:
        return member.project
    else:
        return -1


# TODO Run This function in 1 am
def calculate_task_total_time_in_last_day():
    yesterday = (datetime.now() - timedelta(1)).date()
    year, month, yesterday = str(yesterday).split('-')
    year, month, yesterday = int(year), int(month), int(yesterday)
    all_records_last_day = list(WorkTimeRecord.objects.filter(year=year,
                                                              month=month,
                                                              day=yesterday))
    all_tasks_worked_on_last_day = {}
    for wtr in all_records_last_day:
        if wtr.task not in all_tasks_worked_on_last_day.keys():
            all_tasks_worked_on_last_day[wtr.task] = wtr.duration
        else:
            all_tasks_worked_on_last_day[wtr.task] = all_tasks_worked_on_last_day[wtr.task] + wtr.duration

    for task in all_tasks_worked_on_last_day.keys():
        TaskDailyReporting.objects.create(task=task, year=year, month=month,
                                          day=yesterday, total_time_seconds=all_tasks_worked_on_last_day[task])
    return all_tasks_worked_on_last_day


def calculate_project_total_time_in_day():
    yesterday = (datetime.now() - timedelta(1)).date()
    year, month, yesterday = str(yesterday).split('-')
    year, month, yesterday = int(year), int(month), int(yesterday)
    all_records_last_day = list(TaskDailyReporting.objects.filter(year=year,
                                                                  month=month,
                                                                  day=yesterday))
    all_projects_worked_on_last_day = {}
    for wtr in all_records_last_day:
        if wtr.task.project not in all_projects_worked_on_last_day.keys():
            all_projects_worked_on_last_day[wtr.task.project] = wtr.total_time_seconds
        else:
            all_projects_worked_on_last_day[wtr.task.project] = all_projects_worked_on_last_day[
                                                            wtr.task.project] + wtr.total_time_seconds

    for project in all_projects_worked_on_last_day.keys():
        ProjectDailyReporting.objects.create(project=project, year=year, month=month,
                                             day=yesterday, total_time_seconds=all_projects_worked_on_last_day[project])
    return all_projects_worked_on_last_day
