from django.test import Client, TestCase
from django.urls import reverse_lazy
from task_manager.users.mixins import load_data
from .models import User
from django.utils.translation import gettext as _


class UserTestCase(TestCase):
    fixtures = [
        'user.json',
        'status.json',
        'task.json',
        'label.json',
        'auth.json'
    ]
    test_user = load_data('user_data.json')

    def setUp(self) -> None:
        self.client = Client()

        self.user1 = User.objects.get(pk=4)
        self.user2 = User.objects.get(pk=6)
        self.user3 = User.objects.get(pk=7)

        self.users = User.objects.all()
        self.count = User.objects.count()


class TestCreateUser(UserTestCase):
    def test_create_valid_user(self) -> None:
        user_data = self.test_user['create']['valid'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )

    def test_create_invalid_username(self) -> None:
        user_data = self.test_user['create']['invalid'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('username', errors)
        self.assertEqual(
            [_('Enter a valid username. This value may contain only '
               'letters, numbers, and @/./+/-/_ characters.')],
            errors['username']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_username_exists(self) -> None:
        user_data = self.test_user['create']['exists'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('username', errors)
        self.assertEqual(
            [_('A user with that username already exists.')],
            errors['username']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_dont_match(self) -> None:
        user_data = self.test_user['create']['pass_not_match'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('password2', errors)
        self.assertEqual(
            [_('The two password fields didn’t match.')],
            errors['password2']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_too_short(self) -> None:
        user_data = self.test_user['create']['pass_too_short'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('password2', errors)
        self.assertEqual(
            [_('This password is too short. '
               'It must contain at least 3 characters.')],
            errors['password2']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)


class TestUpdateUser(UserTestCase):
    def test_update_self(self) -> None:
        self.client.force_login(self.user2)

        user_data = self.test_user['update'].copy()
        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': 6}),
            data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))

        self.assertEqual(User.objects.count(), self.count)
        self.assertEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data['first_name']
        )

    def test_update_other(self) -> None:
        self.client.force_login(self.user1)

        user_data = self.test_user['update'].copy()
        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': 6}),
            data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))

        self.assertEqual(User.objects.count(), self.count)
        self.assertNotEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data['first_name']
        )


class TestDeleteUser(UserTestCase):
    def test_delete_self(self) -> None:
        self.client.force_login(self.user2)

        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': self.user2.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))

    def test_delete_other(self) -> None:
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 6})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        self.assertEqual(User.objects.count(), self.count)

    def test_delete_bound_user(self) -> None:
        self.client.force_login(self.user3)

        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 7})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('user_list'))
        self.assertEqual(User.objects.count(), self.count)
