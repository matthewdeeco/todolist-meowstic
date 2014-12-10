from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from todo.views import index_page, home_page, login_page

class IndexPageTest(TestCase):

    def create_and_login_user(self, username='mdco', password='password'):
        User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)

    def test_root_url_resolves_to_index_page(self):
        found = resolve('/')
        self.assertEqual(found.func, index_page)

    def test_index_page_redirects_to_login_page_if_not_logged_in(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_index_page_redirects_to_home_page_if_logged_in(self):
        self.create_and_login_user()
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'home.html')

class LoginPageTest(TestCase):

    def test_login_page_redirects_to_home_page_if_valid_credentials(self):
        User.objects.create_user(username='mdco', password='password', email='mdco@example.com')
        response = self.client.post('/login/', data={'username':'mdco', 'password':'password'}, follow=True)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_page_does_not_redirect_if_invalid_credentials(self):
        response = self.client.post('/login/', data={'username':'mdco', 'password':'password'}, follow=True)
        self.assertTemplateUsed(response, 'login.html')


class SignupPageTest(TestCase):

    def post_to_signup_page(self, *credentials):
        data = dict()
        defaults = {'username':'mdco', 'password1':'password', 'password2':'password', 'email':'mdco@example.com', 'first_name':'Matthew', 'last_name':'Co'}
        for key, value in defaults.items():
            if key in credentials:
                data[key] = value
        response = self.client.post('/signup/', data=data, follow=True)
        return response

    def test_signup_page_can_create_new_user_and_redirects_to_signup_success_page(self):
        response = self.post_to_signup_page('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
        try:
            mdco = User.objects.get(username='mdco')
            self.assertTemplateUsed(response, 'signup_success.html')
        except ObjectDoesNotExist:
            self.fail('User mdco must have been created')

    def assertRaiseErrorAndNoRedirect(self, response):
        with self.assertRaises(ObjectDoesNotExist):
            mdco = User.objects.get(username='mdco')
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_page_no_user_created_if_missing_username_and_does_not_redirect(self):
        response = self.post_to_signup_page('password1', 'password2', 'email', 'first_name', 'last_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_missing_password1_and_does_not_redirect(self):
        response = self.post_to_signup_page('username', 'password2', 'email', 'first_name', 'last_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_missing_password2_and_does_not_redirect(self):
        response = self.post_to_signup_page('username', 'password1', 'email', 'first_name', 'last_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_missing_email_and_does_not_redirect(self):
        response = self.post_to_signup_page('username', 'password1', 'password2', 'first_name', 'last_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_missing_first_name_and_does_not_redirect(self):
        response = self.post_to_signup_page('username', 'password1', 'password2', 'email', 'last_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_missing_last_name_and_does_not_redirect(self):
        response = self.post_to_signup_page('username', 'password1', 'password2', 'email', 'first_name')
        self.assertRaiseErrorAndNoRedirect(response)

    def test_signup_page_no_user_created_if_passwords_do_not_match_and_does_not_redirect(self):
        password1 = 'password'
        password2 = 'password2'
        response = self.client.post('/signup/', data={'username':'mdco', 'password1':password1, 'password2':password2, 'email':'mdco@example.com', 'first_name':'Matthew', 'last_name':'Co'}, follow=True)
        self.assertRaiseErrorAndNoRedirect(response)