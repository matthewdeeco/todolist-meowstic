from selenium import webdriver
from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

class NewVisitorTest(TestCase):
	def setUp(self):
		# self.browser = webdriver.Firefox()
		pass
	
	def tearDown(self):
		# self.browser.quit()
		pass

	def testTodoInBrowserTitle(self):
		pass
		# self.browser.get('http://127.0.0.1:8000/')
		# self.assertIn('To-Do', self.browser.title)
	
	def testIndexPageExists(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)

	def testAdminPageExists(self):
		pass
		# match = resolve('/admin/')
		# print(match.url_name)
		# response = self.client.get('')
		# print(response.status_code)