from django.urls import reverse
from django_seed import Seed
from rest_framework.test import APITestCase

from time_tracker.models import Project, Task, WorkTimeRecord
from django.contrib.auth.models import User

seeder = Seed.seeder()


class BooksTestCase(APITestCase):
    def test_list_books(self):
        # Add dummy data to the Author and Book Table
        # seeder.add_entity(User, 5)
        # users = User.objects.all()
        # print(users, '* '*10)
        seeder.add_entity(Project, 5)
        seeder.add_entity(Task, 10)
        seeder.add_entity(WorkTimeRecord, 100)
        inserted_pks = seeder.execute()
        print()
        print()
        print('* ' * 30)
        print(inserted_pks)
        print('* ' * 30)
        # projects = Project.objects.all()
        # print(projects, '* '*30)
        # we expect the result in 1 query
        with self.assertNumQueries(1):
            # response = self.client.get(reverse("working_time_records"), format="json")
            response = self.client.get(reverse('projects'), format="json")
