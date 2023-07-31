from django.test import Client, TestCase
from task_manager.statuses.models import Statuses
from task_manager.users.mixins import load_data
from task_manager.users.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class StatusTestCase(TestCase):
    fixtures = [
        'user.json',
        'status.json',
        'task.json',
        'label.json',
        'auth.json'
    ]
    test_status = load_data('status_data.json')

    def setUp(self) -> None:
        self.client = Client()

        self.status1 = Statuses.objects.get(pk=1)
        self.status2 = Statuses.objects.get(pk=4)
        self.status3 = Statuses.objects.get(pk=6)
        self.statuses = Statuses.objects.all()
        self.count = Statuses.objects.count()

        self.user1 = User.objects.get(pk=4)

        self.client.force_login(self.user1)


class TestCreateStatus(StatusTestCase):
    def test_create_valid_status(self) -> None:
        status_data = self.test_status['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('create_status'),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))

        self.assertEqual(Statuses.objects.count(), self.count + 1)
        self.assertEqual(
            Statuses.objects.last().name,
            status_data['name']
        )

    def test_create_status_exists(self) -> None:
        status_data = self.test_status['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('create_status'),
            data=status_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Statuses with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.count(), self.count)


class TestUpdateStatus(StatusTestCase):
    def test_update_status(self) -> None:
        status_data = self.test_status['update'].copy()
        response = self.client.post(
            reverse_lazy('update_status', kwargs={'pk': 4}),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))

        self.assertEqual(Statuses.objects.count(), self.count)
        self.assertEqual(
            Statuses.objects.get(id=self.status2.id).name,
            status_data['name']
        )

    def test_update_status_not_logged_in(self) -> None:
        self.client.logout()

        status_data = self.test_status['update'].copy()
        response = self.client.post(
            reverse_lazy('update_status', kwargs={'pk': 4}),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Statuses.objects.count(), self.count)
        self.assertNotEqual(
            Statuses.objects.get(id=self.status2.id).name,
            status_data['name']
        )


class TestDeleteStatus(StatusTestCase):
    def test_delete_status(self) -> None:
        response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': 6})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))
        self.assertEqual(Statuses.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Statuses.objects.get(id=self.status3.id)

    def test_delete_status_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': 6})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Statuses.objects.count(), self.count)

    def test_delete_bound_status(self) -> None:
        response = self.client.post(
            reverse_lazy('delete_status', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('status_list'))
        self.assertEqual(Statuses.objects.count(), self.count)
