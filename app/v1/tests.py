from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import User


from rest_framework.test import APIClient, APITestCase

class TokenTests(APITestCase):
    """
    Проверка получения токена
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='name_1', password='pass_1', is_active=True)  # login User

    def test_get_token_not_auth(self):
        """
        Проверка получения токена неавторизованным пользователем.
        :return:
        """
        client= APIClient()
        data = {'username':'name_1',
                'password':'pass_1',
                }
        response = client.post('/api/token/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.json())

class AccountListCreateTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_post_user(self):
        client = APIClient()
        client.force_authenticate(user=None)

        # Сохранения корректноq формы
        correct_data = {
            'username':'name_1',
            'password':'pass_1',
            'is_active':True,
        }
        response = client.post('/api/v1/users/', data=correct_data)
        self.assertEqual(User.objects.count(),1)
        # Правильность формы ответа
        serializer_read_data = ('id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser')
        for item in serializer_read_data:
            self.assertTrue(item in response.json(), msg=f'{item} нет в ответе')
            self.assertEqual(len(serializer_read_data), 7)
        # Обязатлеьность поля is_active
        uncorrect_data = {
            'username':'name_1',
            'password':'pass_1',
        }

        response_uncoorect = client.post('/api/v1/users/', data=uncorrect_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response_uncoorect.status_code, 400)


class AccountRetrieveUpdateDestroyTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(username='name_1', password='pass_1', is_active=True)


    def test_to_destroy(self):
        client = APIClient()
        # Невозможность удалить несвою форму
        response = client.delete('/api/v1/users/1/')
        self.assertEqual(response.status_code, 401)

        client.force_authenticate(user=None)
        response = client.delete('/api/v1/users/1/')
        self.assertEqual(response.status_code, 401)
        # При удалении запись сновавится не активной, и не удаляется
        user=User.objects.get(id='1')
        client.force_authenticate(user=user)
        response = client.delete('/api/v1/users/1/')
        self.assertEqual(response.status_code, 204)

        user = User.objects.get(id='1')
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.count(),1)


