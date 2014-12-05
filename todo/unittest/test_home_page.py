from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from todo.views import home_page

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

	def test_home_page_can_save_post_request(self):
		new_item_text = 'A new list item'
		request = HttpRequest()
		request.method = 'POST'
		request.POST['new_item_text'] = new_item_text

		response = home_page(request)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, new_item_text)

		self.assertIn(new_item_text, response.content.decode())
		expected_html = render_to_string('home.html', {'new_item_text' : new_item_text})
		self.assertEqual(response.content.decode(), expected_html)