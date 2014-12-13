from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

from todo.views import login_page, home_page
from todo.models import Item

class ItemModelTestCase(TestCase):

    def create_and_login_user(self, username='mdco', password='password'):
        user = User.objects.create_user(username=username, password=password, email='mdco@example.com')
        self.client.login(username=username, password=password)
        return user


class NewItemTest(ItemModelTestCase):

    def test_can_save_new_item_request(self):
        new_item_text = 'A new list item'
        self.create_and_login_user()
        response = self.client.post('/home/new_item', data={'new_item_text' : new_item_text})

        # item must have been added to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_show_home_page_on_new_item(self):
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
        self.assertEqual(item.marked_on, date.today())
        # completed items must be set to uncomplete after another toggle
        response = self.client.post('/home/toggle_complete_item', data={'item_id' : 1})
        item = Item.objects.get(id=1)
        self.assertFalse(item.completed)


class CancelItemTest(ItemModelTestCase):

    def test_can_save_cancel_request(self):
        user = self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        response = self.client.get('/home/cancel_item/1')
        item = Item.objects.get(id=1)
        self.assertTrue(item.cancelled)

    def test_can_only_cancel_own_items(self):
        mdco = self.create_and_login_user(username='mdco')
        Item.objects.create(text='A new list item', user=mdco)
        Item.objects.create(text='Item number 2', user=mdco)
        response = self.client.get('/home/cancel_item/1')
        item = Item.objects.get(id=1)
        self.assertTrue(item.cancelled)

        spfestin = self.create_and_login_user(username='spfestin')
        response = self.client.get('/home/cancel_item/2')
        item = Item.objects.get(id=2)
        self.assertFalse(item.cancelled)


class DeleteItemTest(ItemModelTestCase):

    def test_can_save_delete_request(self):
        user =  self.create_and_login_user()
        Item.objects.create(text='A new list item', user=user)
        response = self.client.get('/home/delete_item/1')
        with self.assertRaises(ObjectDoesNotExist):
            item = Item.objects.get(id=1)

    def test_can_only_delete_own_items(self):
        mdco = self.create_and_login_user(username='mdco')
        Item.objects.create(text='A new list item', user=mdco)
        Item.objects.create(text='Item number 2', user=mdco)
        response = self.client.get('/home/delete_item/1')
        with self.assertRaises(ObjectDoesNotExist):
            item = Item.objects.get(id=1)

        spfestin = self.create_and_login_user(username='spfestin')
        response = self.client.get('/home/delete_item/2')
        try:
            item = Item.objects.get(id=2)
        except ObjectDoesNotExist:
            self.fail('Item 2 must not have been deleted!')
            pass

class DueItemTest(ItemModelTestCase):

    def test_check_if_item_is_due(self):
        mdco = self.create_and_login_user(username='mdco')
        today = date.today()
        item = Item.objects.create(text='A new list item', user=mdco, due_on=today)
        self.assertTrue(item.due())

    def test_count_days_before_item_is_due(self):
        mdco = self.create_and_login_user(username='mdco')
        today = date.today()
        tomorrow = date.fromordinal(today.toordinal()+1)
        item = Item.objects.create(text='A new list item', user=mdco, due_on=tomorrow)
        self.assertEqual(item.due_in(), 1)

    def test_count_days_since_item_was_due(self):
        mdco = self.create_and_login_user(username='mdco')
        today = date.today()
        yesterday = date.fromordinal(today.toordinal()-1)
        item = Item.objects.create(text='A new list item', user=mdco, due_on=yesterday)
        self.assertTrue(item.overdue())
        self.assertEqual(item.overdue_by(), 1)
        
