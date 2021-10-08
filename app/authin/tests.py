from app.authin.models import User

from rest_framework.test import APIClient, APITestCase


class TokenTests(APITestCase):
    """
    Проверка получения токена
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username='name_1', password='pass_1',
                                 is_active=True)

    def test_get_token_not_auth(self):
        """
        Проверка получения токена неавторизованным пользователем.
        :return:
        """
        client = APIClient()
        data = {'username': 'name_1',
                'password': 'pass_1',
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

        # Сохранения корректноя формы
        correct_data = {
            'username': 'name_1',
            'password': 'pass_1',
            'is_active': True,
        }
        response = client.post('/api/authin/users/', data=correct_data)
        self.assertEqual(User.objects.count(), 1)
        # Правильность формы ответа
        serializer_read_data = ('id', 'username', 'first_name', 'last_name',
                                'is_active', 'last_login', 'is_superuser')
        for item in serializer_read_data:
            self.assertTrue(item in response.json(), msg=f'{item} нет')
            self.assertEqual(len(serializer_read_data), 7)
        # Обязатлеьность поля is_active
        incorrect_data = {
            'username': 'name_1',
            'password': 'pass_1',
        }

        response_incorrect = client.post('/api/authin/users/', data=incorrect_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response_incorrect.status_code, 400)


class AccountRetrieveUpdateDestroyTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(username='name_1', password='pass_1',
                            is_active=True)

    def test_to_destroy(self):
        client = APIClient()
        # Невозможность удалить несвою форму
        response = client.delete('/api/authin/users/1/')
        self.assertEqual(response.status_code, 401)

        client.force_authenticate(user=None)
        response = client.delete('/api/authin/users/1/')
        self.assertEqual(response.status_code, 401)
        # При удалении запись сновавится не активной, и не удаляется
        user = User.objects.get(id='1')
        client.force_authenticate(user=user)
        response = client.delete('/api/authin/users/1/')
        self.assertEqual(response.status_code, 204)
        #
        user = User.objects.get(id='1')
        self.assertFalse(user.is_active)
        self.assertEqual(User.objects.count(), 1)

        superuser = User.objects.create(username='admin', password='admin',
                                        is_active=True, is_superuser=True)
        client.force_authenticate(user=superuser)

        response = client.patch('/api/authin/users/1/', is_active=True)
        self.assertEqual(response.status_code, 200)
