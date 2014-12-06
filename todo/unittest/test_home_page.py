from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from todo.views import login_page, home_page
from todo.models import Item

class HomePageTest(TestCase):

    def login_user(self, username='mdco', password='password'):
        User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)
    
    def test_home_page_redirects_to_login_page_if_user_is_not_logged_in(self):
        response = self.client.get('/home/', follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_home_page_exists(self):
        self.login_user()
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_can_save_post_request(self):
        new_item_text = 'A new list item'

        self.login_user()
        response = self.client.post('/home/', data={'new_item_text' : new_item_text})

        # item must have been added to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_user_still_at_home_page_after_post(self):
        self.login_user()
        response = self.client.post('/home/', data={'new_item_text' : 'item 1'}, follow=True)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_displays_all_list_items(self):
        new_item_texts = ['item 1', 'item 2']
        Item.objects.create(text=[text for text in new_item_texts])
        
        self.login_user()
        response = self.client.get('/home/')
        
        for text in new_item_texts:
            self.assertContains(response, text)