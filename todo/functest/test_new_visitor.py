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

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('item_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.address)
        new_item_texts = ['Submit CS 145 Machine Problem', 'Submit CS 180 Machine Problem']

        # Input 2 items
        for new_item_text in new_item_texts:
            inputbox = self.browser.find_element_by_id('new_item')
            inputbox.send_keys(new_item_text)
            inputbox.send_keys(Keys.ENTER)

        # Check that all items have been added
        for new_item_text in new_item_texts:
            self.check_for_row_in_list_table(new_item_text)
