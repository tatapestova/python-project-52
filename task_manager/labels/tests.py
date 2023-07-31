from django.test import Client, TestCase
from task_manager.users.mixins import load_data
from task_manager.users.models import User
from task_manager.labels.models import Labels
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class LabelTestCase(TestCase):
    fixtures = [
        'user.json',
        'status.json',
        'task.json',
        'label.json',
        'auth.json'
    ]
    test_label = load_data('label_data.json')

    def setUp(self) -> None:
        self.client = Client()

        self.label1 = Labels.objects.get(pk=2)
        self.label2 = Labels.objects.get(pk=3)
        self.label3 = Labels.objects.get(pk=4)
        self.labels = Labels.objects.all()
        self.count = Labels.objects.count()

        self.user1 = User.objects.get(pk=4)

        self.client.force_login(self.user1)


class TestCreateLabel(LabelTestCase):
    def test_create_valid_label(self) -> None:
        label_data = self.test_label['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))

        self.assertEqual(Labels.objects.count(), self.count + 1)
        self.assertEqual(
            Labels.objects.last().name,
            label_data['name']
        )

    def test_create_label_exists(self) -> None:
        label_data = self.test_label['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.count(), self.count)


class TestUpdateLabel(LabelTestCase):
    def test_update_label(self) -> None:
        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))

        self.assertEqual(Labels.objects.count(), self.count)
        self.assertEqual(
            Labels.objects.get(id=self.label1.id).name,
            label_data['name']
        )

    def test_update_label_not_logged_in(self) -> None:
        self.client.logout()

        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Labels.objects.count(), self.count)
        self.assertNotEqual(
            Labels.objects.get(id=self.label2.id).name,
            label_data['name']
        )


class TestDeleteLabel(LabelTestCase):
    def test_delete_label(self) -> None:
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Labels.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Labels.objects.get(id=self.label2.id)

    def test_delete_label_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Labels.objects.count(), self.count)

    def test_delete_bound_label(self) -> None:
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 4})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Labels.objects.count(), self.count)
