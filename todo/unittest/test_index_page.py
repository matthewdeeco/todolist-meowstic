from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.contrib.auth.models import User

from todo.views import index_page, home_page, login_page

class IndexPageTest(TestCase):

    def login_user(self, username='mdco', password='password'):
        User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)

    def test_root_url_resolves_to_index_page(self):
        found = resolve('/')
        self.assertEqual(found.func, index_page)

    def test_index_page_redirects_to_login_page_if_not_logged_in(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_index_page_redirects_to_home_page_if_logged_in(self):
        self.login_user()
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