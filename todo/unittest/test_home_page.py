from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from todo.views import home_page
from todo.models import Item

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_exists(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_can_save_post_request(self):
        new_item_text = 'A new list item'
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_item_text'] = new_item_text

        response = home_page(request)

        # item must have been added to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_home_page_redirects_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['new_item_text'] = 'item 1'

        response = home_page(request)

        # user should be redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_displays_all_list_items(self):
        new_item_texts = ['item 1', 'item 2']
        Item.objects.create(text=[text for text in new_item_texts])
        request = HttpRequest()

        response = home_page(request)
        
        for text in new_item_texts:
            self.assertIn(text, response.content.decode())