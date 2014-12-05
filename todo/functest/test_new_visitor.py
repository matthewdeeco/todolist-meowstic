from django.test import TestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(2)
		self.address = 'http://localhost:8000'

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.address)
		# Find the input box
		inputbox = self.browser.find_element_by_id('new_item')
		# Check title
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		# Try inputting a new item
		new_item_text = 'Submit CS 145 Machine Problem'
		inputbox.send_keys(new_item_text)
		inputbox.send_keys(Keys.ENTER)
		# Check that the item appears in the list
		table = self.browser.find_element_by_id('item_list')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(new_item_text, [row.text for row in rows])

		self.fail('Finish the test!')
		pass
