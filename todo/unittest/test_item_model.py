from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import date

from todo.views import login_page, home_page
from todo.models import Item

class ItemModelTestCase(TestCase):

    def create_and_login_user(self, username='mdco', password='password'):
        user = User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)
        return user


class NewItemTest(ItemModelTestCase):

    def test_can_save_post_request(self):
        new_item_text = 'A new list item'
        self.create_and_login_user()
        response = self.client.post('/home/new_item', data={'new_item_text' : new_item_text})

        # item must have been added to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_show_home_page_on_post(self):
        self.create_and_login_user()
        response = self.client.post('/home/new_item', data={'new_item_text': 'A new list item'}, follow=True)
        self.assertTemplateUsed(response, 'home.html')


class CompleteItemTest(ItemModelTestCase):

    def test_can_save_post_request(self):
        user =  self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        # uncompleted items must be set to complete after a toggle
        response = self.client.post('/home/toggle_complete_item', data={'item_id' : 1})
        item = Item.objects.get(id=1)
        self.assertTrue(item.completed)
        self.assertEqual(item.completed_on, date.today())
        # completed items must be set to uncomplete after another toggle
        response = self.client.post('/home/toggle_complete_item', data={'item_id' : 1})
        item = Item.objects.get(id=1)
        self.assertFalse(item.completed)

    def test_show_home_page_on_post(self):
        user=self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        response = self.client.post('/home/toogle_complete_item', data={'item_id' : 1}, follow=True)
        self.assertTemplateUsed(response, 'home.html')


class CancelItemTest(ItemModelTestCase):

    def test_can_save_post_request(self):
        user =  self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        response = self.client.get('/home/cancel_item/1')
        item = Item.objects.get(id=1)
        self.assertTrue(item.cancelled)

    def test_show_home_page_on_post(self):
        user=self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        response = self.client.post('/home/cancel_item', data={'item_id' : 1}, follow=True)
        self.assertTemplateUsed(response, 'home.html')