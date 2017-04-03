from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


def create_user():
    return User.objects.create_user('alice', 'alice@example.com', 'secret')


class LoginTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_front_page_redirects_to_login_page(self):
        response = self.client.get('/')

        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            response['Location'], '/account/login/?next=/')

    def test_login_page_includes_email_and_password_fields(self):
        response = self.client.get('/account/login/')

        self.assertEquals(response.status_code, 200)
        self.assertIn('Email', response.content)
        self.assertIn('Password', response.content)

    def test_successful_login_redirects_to_front_page(self):
        response = self.client.post(
            '/account/login/',
            {'email': 'alice@example.com', 'password': 'secret'})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], '/')

    def test_failed_login_shows_error_on_login_page(self):
        response = self.client.post(
            '/account/login/',
            {'email': 'alice@example.com', 'password': 'wrong'})

        self.assertEquals(response.status_code, 200)
        self.assertIn(
            'Please enter a correct username and password.', response.content)
