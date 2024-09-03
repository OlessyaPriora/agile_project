from django.test import TestCase
from rest_framework import response, status
from apps.users.models import User
from rest_framework.response import Response
from apps.users.serializers.user_serializers import RegisterUserSerializer
from django.urls import reverse
from apps.projects.models import Project


class UserListTests(TestCase):
# get users list
    def test_user_list(self):
        User.objects.bulk_create([
            User(username='fiona', first_name='Fiona', last_name='Cartoon', email='fiona@gmail.com',
                 position='CEO', password='fionafiona'),
            User(username='bob', first_name='bob', last_name='bob', email='bob@gmail.com',
                 position='Programmer', password='bobbobbob'),
            User(username='shark', first_name='shark', last_name='shark', email='shark@gmail.com',
                 position='Programmer', password='sharkshark'),
            User(username='marley', first_name='marley', last_name='marley', email='marley@gmail.com',
                 position='CEO', password='marleymarley'),
        ])

        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 4)


class RegisterUserTests(TestCase):
    def setUp(self):
        self.url = '/api/v1/users/register/'
        self.data = {
            'username': 'fiona',
            'first_name': 'Fiona',
            'last_name': 'Cartoon',
            'email': 'fiona@gmail.com',
            'position': 'CEO',
            'password': 'fionafiona',
            're_password': 'fionafiona',
        }

# new user registration
    def test_user_register(self):
        response = self.client.post(self.url, self.data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(User.objects.count(), 1)
        print(response.json)

    def test_user_invalid_email(self ):
        self.data['email'] = 'sendy'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_user_invalid_register_position(self):
        self.data['position'] = 'SENIOR'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)

    def test_user_register_password_mismatch(self):
        self.data['re_password'] = ',fhgcgf87676'
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 400)


# Validation checking
class RegisterUserSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'fiona',
            'first_name': 'Fiona',
            'last_name': 'Cartoon',
            'email': 'fiona@gmail.com',
            'position': 'CEO',
            'password': 'fionafiona',
            're_password': 'fionafiona',
        }

    def test_valid_user_data(self):
        serializer = RegisterUserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsInstance(serializer.validated_data['username'], str)
        self.assertIsInstance(serializer.validated_data['first_name'], str)
        self.assertIsInstance(serializer.validated_data['last_name'], str)
        self.assertIsInstance(serializer.validated_data['position'], str)
        self.assertIsInstance(serializer.validated_data['email'], str)
        self.assertIsInstance(serializer.validated_data['password'], str)
        self.assertIsInstance(serializer.validated_data['re_password'], str)

#checking possible errors
    def test_valid_username(self):
        self.data['username'] = 'fiona,fi'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The username must be alphanumeric characters or have only _ symbol',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_first_name(self):
        self.data['first_name'] = 'Fiona22'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The first name must contain only alphabet symbols',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_last_name(self):
        self.data['last_name'] = 'Cartoon22'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            'The last name must contain only alphabet symbols',
            [str(i) for i in serializer.errors['non_field_errors']])

    def test_valid_password(self):
        self.data['re_password'] = 'jhfhgdgf6545.'
        serializer = RegisterUserSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Passwords don't match")


# Task2
# Writing code for a user object via BDD + TDD
# Based on the script you created, write tests for:
class UserInformationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='fiona',
            first_name='Fiona',
            last_name='Cartoon',
            email='fiona@gmail.com',
            phone='1234567890',
            position='CEO',
            project=Project.objects.create(name='Fiona project')
        )

    def test_get_user_detail(self):
        response = self.client.get('/api/v1/users/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data['username'], str)
        self.assertIsInstance(response.data['first_name'], str)
        self.assertIsInstance(response.data['last_name'], str)
        self.assertIsInstance(response.data['email'], str)
        self.assertIsInstance(response.data['phone'], str)
        self.assertIsInstance(response.data['position'], str)
        self.assertIsInstance(response.data['project'], str)

        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['phone'], self.user.phone)
        self.assertEqual(response.data['position'], self.user.position)
        self.assertEqual(response.data['project'], self.user.project.name)

    def test_get_user_detail_not_found(self):
        response = self.client.get('/api/v1/users/33/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data, 'No User matches the given query')