from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from todo.views import login_page, home_page
from todo.models import Item

class HomePageTest(TestCase):

    def create_and_login_user(self, username='mdco', password='password'):
        User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)
    
    def test_home_page_redirects_to_login_page_if_user_is_not_logged_in(self):
        response = self.client.get('/home/', follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_home_page_exists(self):
        self.create_and_login_user()
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_user_items_not_visible_to_others(self):
        new_item_texts = ['item 1', 'item 2']
        self.create_and_login_user(username='mdco')
        user_mdco = authenticate(username='mdco', password='password')
        Item.objects.create(text=[text for text in new_item_texts], user=user_mdco)
        response = self.client.get('/home/')
        
        for text in new_item_texts:
            self.assertContains(response, text)

        self.create_and_login_user(username='spfestin')
        response = self.client.get('/home/')
        
        for text in new_item_texts:
            self.assertNotContains(response, text)