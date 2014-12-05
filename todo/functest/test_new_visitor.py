from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('item_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def input_new_item(self, text):
        inputbox = self.browser.find_element_by_id('new_item_text')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        texts = ['item 1', 'item 2']

        self.input_new_item(texts[0])
        self.browser.implicitly_wait(5)
        self.check_for_row_in_list_table(texts[0])

        self.input_new_item(texts[1])
        self.browser.implicitly_wait(5)
        self.check_for_row_in_list_table(texts[0])
        self.check_for_row_in_list_table(texts[1])