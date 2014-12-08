from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def login_user(self, username, password='password'):
        username_box = self.browser.find_element_by_id('username')
        username_box.send_keys(username)
        password_box = self.browser.find_element_by_id('password')
        password_box.send_keys(password)
        password_box.send_keys(Keys.ENTER)

    def logout(self):
        logout_link = self.browser.find_element_by_id('logout')
        logout_link.click()

    def check_for_item_in_item_list(self, item_text):
        item_list = self.browser.find_element_by_id('item_list')
        items = item_list.find_elements_by_class_name('item_text')
        self.assertIn(item_text, [item.text for item in items])

    def get_checkbox_for(self, target_item_text):
        item_list = self.browser.find_element_by_id('item_list')
        item_rows = item_list.find_elements_by_class_name('todo_item')
        for item_row in item_rows:
            item_text = item_row.find_elements_by_class_name('item_text')
            if target_item_text == item_text[0].text:
                item_checkbox = item_row.find_elements_by_tag_name('input')
                return item_checkbox[0]

    def input_new_item(self, text):
        inputbox = self.browser.find_element_by_id('new_item_text')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        mdco_items = ['item 1', 'item 2']

        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        self.input_new_item(mdco_items[0])
        self.check_for_item_in_item_list(mdco_items[0])

        # check that both items are visible in the page
        self.input_new_item(mdco_items[1])
        self.browser.implicitly_wait(5)
        self.check_for_item_in_item_list(mdco_items[0])
        self.check_for_item_in_item_list(mdco_items[1])

        # switch to user spfestin
        self.logout()
        User.objects.create_user(username='spfestin', password='password', first_name='Susan')
        self.login_user('spfestin')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(mdco_items[0], page_text)
        self.assertNotIn(mdco_items[1], page_text)
        
        spfestin_item = 'item 3'
        self.input_new_item(spfestin_item)

        # list from mdco must still not be viewable, but spfestin's is
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(mdco_items[0], page_text)
        self.assertNotIn(mdco_items[1], page_text)
        self.assertIn(spfestin_item, page_text)

    def test_can_mark_item_as_complete_and_retrieve_it_later(self):
        mdco_items = ['item 1', 'item 2']

        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        self.input_new_item(mdco_items[0])
        self.input_new_item(mdco_items[1])
        checkbox1 = self.get_checkbox_for(mdco_items[0])
        checkbox1.click()

        # logout and login again
        self.logout()
        self.login_user('mdco')

        checkbox1 = self.get_checkbox_for(mdco_items[0])
        self.assertTrue(checkbox1.is_selected())
        checkbox2 = self.get_checkbox_for(mdco_items[1])
        self.assertFalse(checkbox2.is_selected())