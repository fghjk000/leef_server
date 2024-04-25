from django.test import TestCase
from rest_framework.test import APIClient
from leef.models import User, Token
from django.urls import reverse


class UserCreateAPI(TestCase):
    client_class: APIClient = APIClient

    @classmethod
    def setUpTestData(cls):
        from leef.models import User
        cls.user = User.objects.create(
            name="test_name",
            nickname='test_nick'
        )

    def test_유저목록(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)
        response_date: list[dict] = response.json()
        self.assertEqual(len(response_date), 1)
        self.assertEqual(response_date[0]['id'], self.user.id)
        self.assertEqual(response_date[0]['name'], self.user.name)
        self.assertEqual(response_date[0]['nickname'], self.user.nickname)
        self.assertEqual(response_date[0]['password'], self.user.password)
        expect_data = ['id', 'name', 'nickname', 'password']

    def test_유저생성(self):
        response = self.client.post('/user/', data={
            'name': 'test_name',
            'nickname': 'test_nick'
        })
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['name'], response_data['name'])
        self.assertEqual(response_data['nickname'], response_data['nickname'])
        self.assertTrue(User.objects.filter(id=response_data['id']).exists())


class UserDetailAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        from leef.models import User
        cls.user = User.objects.create(
            name="test_name",
            nickname='test_nick'
        )

    def test_유저상세목록(self):
        response = self.client.get(f'/user/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 5)

    def test_유저정보수정(self):
        test_name = {'name': 'test_name'}
        test_nickname = {'nickname': 'test_nick'}

        with self.subTest("name 수정"):
            self.client.patch(f'/user/{self.user.id}', data=test_name)
            self.user.refresh_from_db()
            self.assertEqual(self.user.name, test_name['name'])

        with self.subTest("nickname 수정"):
            self.client.patch(f'/user/{self.user.id}', data=test_nickname)
            self.user.refresh_from_db()
            self.assertEqual(self.user.nickname, test_nickname['nickname'])

    def test_유저탈퇴(self):
        response = self.client.delete(f'/user/{self.user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class TokenCreateAPI(TestCase):
    client_class: APIClient = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(name='test_user', nickname='test_nick', password='pass')
        cls.token = Token.objects.create(user=cls.user, key='1234')

    def test_생성되어있는_유저(self):
        response = self.client.post(reverse('signup'), {
            'username': 'test_user', 'nickname': 'test_nick', 'password': 'pass'})
        self.assertEqual(response.status_code, 401)

    def test_새로운_유저가입(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('signup'), {
            'name': 'new_user', 'nickname': 'new_nick', 'password': 'new_pass'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)


class LogoutAPITest(TestCase):
    client_class: APIClient = APIClient

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(name='logout_user', nickname='logout_nick', password='logout_pass')
        cls.token = Token.objects.create(user=user, key='test_token_key')

    def test_유저로그아웃(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete('/user/logout/', data={'token': self.token.key})
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())


class LoginAPITest(TestCase):
    client_class: APIClient = APIClient

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            name='test_user',
            nickname='test_nick',
            password='test_pass'
        )
        cls.token = Token.objects.create(user=user, key='test_token_key')

    def test_로그인성공(self):
        response = self.client.post('/user/login/', data={
            'name': 'test_user',
            'password': 'test_pass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_로그인실패_잘못된패스워드(self):
        response = self.client.post('/user/login/', data={
            'name': 'test_user',
            'password': 'wrong_pass'
        })
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.data is None or 'token' not in response.data)
