from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from selenium import webdriver

from todo.views import index_page

class IndexPageTest(TestCase):
	def setUp(self):
		# self.browser = webdriver.Firefox()
		pass
	
	def tearDown(self):
		# self.browser.quit()
		pass
	
	def test_root_url_resolves_to_index_page(self):
		found = resolve('/')
		self.assertEqual(found.func, index_page)

	def test_index_page_exists(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)

	def test_index_page_returns_correct_html(self):
		request = HttpRequest()
		response = index_page(request)
		expected_html = render_to_string('index.html')
		self.assertEqual(response.content.decode(), expected_html)