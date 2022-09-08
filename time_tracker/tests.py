import random
from http.client import HTTPException

from django.urls import reverse
from django_seed import Seed
from rest_framework.test import APITestCase
from time_tracker.functions import calculate_task_total_time_in_last_day, calculate_project_total_time_in_day
from time_tracker.models import Project, Task, WorkTimeRecord, InvitedMembers, TaskDailyReporting, ProjectDailyReporting
from django.contrib.auth.models import User
from datetime import datetime, timedelta

seeder = Seed.seeder()


class ProjectTestCase(APITestCase):
    def setUp(self):
        self.project_owner = User.objects.create_user('project_owner', 'project@owner.com', 'project_owner123')
        self.project_member = User.objects.create_user('project_member', 'project@member.com', 'project_member123')
        self.another_member = User.objects.create_user('another_member', 'another@member.com', 'another_member123')
        res = self.client.post('/auth/login', data={'username': 'project_owner', 'password': 'project_owner123'})
        self.token = res.json().get('token')

    def test_false_login_data(self):
        res = self.client.post('/auth/login', data={'username': 'project_owner', 'password': 'project_owner123'})
        self.assertRaisesMessage(res, 'Incorrect Credentials Passed.')

    def test_make_a_new_project(self):
        data = {
            'title': 'new test project',
            'budget': 1000.0,
            'deadline': str(datetime.today().date()),
        }
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}',
        }

        response = self.client.post(path='/api/projects/', data=data, **self.headers)
        self.project_id = response.json().get('id')
        self.assertEquals({
            "id": response.json().get('id'),
            "owner": self.project_owner.id,
            "members": [],
            **data

        }, response.json())

    def test_invite_people_to_project(self):
        self.test_make_a_new_project()
        data = {
            'email': 'another@member.com',
            'project': 1,
            'invitation_code': 0,
        }
        response = self.client.post(reverse('invite_members'), data=data, **self.headers)
        # TODO: In Production Just returns the email and project, NOT RETURN invitation_code IN PRODUCTION!
        self.invitation_code = response.json().get('invitation_code')
        result = {
            'email': 'another@member.com', 'project': 1, 'invitation_code': self.invitation_code
        }
        self.assertEquals(response.json(), result)

    def test_valid_user_response_to_project_invitation(self):
        self.test_invite_people_to_project()
        res = self.client.post('/auth/login', data={'username': 'another_member', 'password': 'another_member123'})
        self.token = res.json().get('token')
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}',
        }
        data = {
            'invitation_code': self.invitation_code,
        }
        res = self.client.put(reverse('invitation_response'), data=data, **self.headers)
        self.assertEquals(res.json(), {"msg": f"welcome to {Project.objects.get(id=1).title}"})

    def test_not_valid_user_response_to_project_invitation(self):
        self.test_invite_people_to_project()
        res = self.client.post('/auth/login', data={'username': 'project_member', 'password': 'project_member123'})
        self.token = res.json().get('token')
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}',
        }
        data = {
            'invitation_code': self.invitation_code,
        }
        with self.assertRaisesMessage(HTTPException, 'You are not invited') as cm:
            self.client.put(reverse('invitation_response'), data=data, **self.headers)

    def test_prevent_not_owner_user_to_add_members(self):
        self.test_make_a_new_project()
        res = self.client.post('/auth/login', data={'username': 'another_member', 'password': 'another_member123'})
        self.token = res.json().get('token')
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {self.token}',
        }
        data = {
            'email': 'project@member.com',
            'project': 1,
            'invitation_code': 0,
        }
        res = self.client.post(reverse('invite_members'), data=data, **self.headers)
        self.assertEquals(res.json(), {'detail': 'You do not have permission to perform this action.'})


class TaskAndProjectTimeTestCase(APITestCase):
    def test_list_projects(self):
        seeder.add_entity(User, 5)
        seeder.execute()
        users = User.objects.all()
        seeder.add_entity(Project, 10, {
            'owner': users[0],
        })
        seeder.execute()
        projects = Project.objects.all()
        seeder.add_entity(Task, 10, {
            'assignee': users[0],
            'project': projects[0],
        })
        seeder.execute()
        tasks = Task.objects.all()
        yesterday = (datetime.now() - timedelta(1)).date()
        year, month, yesterday = str(yesterday).split('-')
        year, month, yesterday = int(year), int(month), int(yesterday)

        for i in range(10):
            time = float(random.randint(1662566177, 1762566177))
            seeder.add_entity(WorkTimeRecord, 1, {
                'year': year,
                'month': month,
                'day': yesterday,
                'task': tasks[0],
                'start_time': time,
                'end_time': time + 60.0,
                'project': projects[0],
                'doer': users[0],
            })
            seeder.execute()
        for i in range(10):
            time = float(random.randint(1662566177, 1762566177))
            seeder.add_entity(WorkTimeRecord, 1, {
                'year': year,
                'month': month,
                'day': yesterday,
                'task': tasks[1],
                'start_time': time,
                'end_time': time + 120.0,
                'project': projects[0],
                'doer': users[0],
            })
            seeder.execute()
        task_time_response = calculate_task_total_time_in_last_day()
        result = {tasks[0]:
                      60 * len(WorkTimeRecord.objects.filter(day=yesterday, month=month, year=year, task=tasks[0])),
                  tasks[1]:
                      120 * len(WorkTimeRecord.objects.filter(day=yesterday, month=month, year=year, task=tasks[1]))
                  }
        # TEST SAVING THE TOTAL TIME SPENT IN TASK1 YESTERDAY
        self.assertEquals(task_time_response[tasks[0]],
                          TaskDailyReporting.objects.get(task__id=tasks[0].id).total_time_seconds)
        # TEST SAVING THE TOTAL TIME SPENT IN TASK2 YESTERDAY
        self.assertEquals(task_time_response[tasks[1]],
                          TaskDailyReporting.objects.get(task__id=tasks[1].id).total_time_seconds)
        self.assertEqual(task_time_response, result)

        project_time_response = calculate_project_total_time_in_day()
        # TEST SAVING THE TOTAL TIME SPENT IN PROJECT1 YESTERDAY
        self.assertEquals(project_time_response[projects[0]],
                          ProjectDailyReporting.objects.get(project__id=projects[0].id).total_time_seconds)
        self.assertEquals({projects[0]: (result[tasks[0]] + result[tasks[1]])}, project_time_response)


class ProjectsRelationWithUsersQueryTest(APITestCase):
    def setUp(self):
        self.project_owner = User.objects.create_user('project_owner', 'project@owner.com', 'project_owner123')
        seeder.add_entity(User, 20)
        user_pks = seeder.execute()
        project = Project.objects.create(title='TEST PROJ', owner=self.project_owner, deadline='2022-09-12',
                                         budget=1000.0)
        all_users = User.objects.all()
        for user in all_users:
            project.members.add(user)
        print(project.members)
        res = self.client.post('/auth/login', data={'username': 'project_owner', 'password': 'project_owner123'})
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Token {res.json().get("token")}',
        }

    def test_num_of_query(self):
        # TODO Find ways to decrease below '5'
        with self.assertNumQueries(5):
            self.client.get(path='/api/projects/', **self.headers)
