from django.test import TestCase, Client
from task_manager.tasks.models import Tasks
from task_manager.users.mixins import load_data
from task_manager.users.models import User
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class TaskTestCase(TestCase):
    fixtures = [
        'user.json',
        'status.json',
        'task.json',
        'label.json',
        'auth.json'
    ]
    test_task = load_data('task_data.json')

    def setUp(self) -> None:
        self.client = Client()

        self.task1 = Tasks.objects.get(pk=1)
        self.task2 = Tasks.objects.get(pk=2)
        self.task3 = Tasks.objects.get(pk=3)
        self.tasks = Tasks.objects.all()
        self.count = Tasks.objects.count()

        self.user1 = User.objects.get(pk=4)
        self.user2 = User.objects.get(pk=6)

        self.status1 = Statuses.objects.get(pk=1)

        self.label2 = Labels.objects.get(pk=2)
        self.labels = Labels.objects.filter(pk=2)

        self.client.force_login(self.user1)


class TestCreateTask(TaskTestCase):
    def test_create_valid_task(self) -> None:
        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))

        self.assertEqual(Tasks.objects.count(), self.count + 1)
        self.assertEqual(
            Tasks.objects.last().name,
            task_data['name']
        )
        self.assertEqual(
            Tasks.objects.last().author,
            self.user1
        )
        self.assertEqual(
            Tasks.objects.last().executor,
            self.user2
        )

    def test_create_task_exists(self) -> None:
        task_data = self.test_task['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Task with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tasks.objects.count(), self.count)


class TestUpdateTask(TaskTestCase):
    def test_update_task(self) -> None:
        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))

        self.assertEqual(Tasks.objects.count(), self.count)
        self.assertEqual(
            Tasks.objects.get(id=self.task2.id).name,
            task_data['name']
        )
        self.assertEqual(
            Tasks.objects.get(id=self.task2.id).executor.id,
            task_data['executor']
        )

    def test_update_task_not_logged_in(self) -> None:
        self.client.logout()

        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Tasks.objects.count(), self.count)
        self.assertNotEqual(
            Tasks.objects.get(id=self.task2.id).name,
            task_data['name']
        )


class TestDeleteTask(TaskTestCase):
    def test_delete_task(self) -> None:
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Tasks.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Tasks.objects.get(id=self.task2.id)

    def test_delete_task_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Tasks.objects.count(), self.count)

    def test_delete_task_unauthorised(self) -> None:
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Tasks.objects.count(), self.count)
