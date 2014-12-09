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
        sleep(1)

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

    def input_new_item(self, text):
        inputbox = self.browser.find_element_by_id('new_item_text')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)
        sleep(1)

    def check_for_item_in_item_list(self, item_text):
        item_list = self.browser.find_element_by_id('item_list')
        items = item_list.find_elements_by_class_name('item_text')
        self.assertIn(item_text, [item.text for item in items])

    def get_checkbox_for(self, item_id):
        sleep(1)
        item_checkbox = self.browser.find_element_by_id('checkbox-' + str(item_id))
        return item_checkbox

    def get_cancel_link_for(self, item_id):
        sleep(1)
        item_row = self.browser.find_element_by_id('item-' + str(item_id))
        dropdown = item_row.find_elements_by_class_name('dropdown-toggle')
        dropdown[0].click()
        cancel_link = item_row.find_elements_by_class_name('cancel_link')
        return cancel_link[0]

    def test_can_start_a_list_and_retrieve_it_later(self):
        mdco_items = ['Buy batteries', 'Email prof']

        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        self.input_new_item(mdco_items[0])
        sleep(1)
        self.check_for_item_in_item_list(mdco_items[0])

        # check that both items are visible in the page
        self.input_new_item(mdco_items[1])
        self.check_for_item_in_item_list(mdco_items[0])
        self.check_for_item_in_item_list(mdco_items[1])

        # switch to user spfestin
        self.logout()
        User.objects.create_user(username='spfestin', password='password', first_name='Susan')
        self.login_user('spfestin')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(mdco_items[0], page_text)
        self.assertNotIn(mdco_items[1], page_text)
        
        spfestin_item = 'Submit Grades'
        self.input_new_item(spfestin_item)

        # list from mdco must still not be viewable, but spfestin's is
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(mdco_items[0], page_text)
        self.assertNotIn(mdco_items[1], page_text)
        self.assertIn(spfestin_item, page_text)

    def test_can_change_item_attributes_and_retrieve_it_later(self):
        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        mdco_items = ['Buy batteries', 'Email prof', 'Call a friend', 'Pass report']
        for item in mdco_items:
            self.input_new_item(item)

        # check item 1 as complete
        checkbox1 = self.get_checkbox_for(1)
        checkbox1.click()
        # check item 2 as complete and then uncheck it
        checkbox2 = self.get_checkbox_for(2)
        checkbox2.click()
        checkbox2 = self.get_checkbox_for(2)
        checkbox2.click()
        # mark item 3 as cancelled
        cancel_link3 = self.get_cancel_link_for(3)
        cancel_link3.click()
        # mark item 4 as cancelled and then unmark it
        cancel_link4 = self.get_cancel_link_for(4)
        cancel_link4.click()
        cancel_link4 = self.get_cancel_link_for(4)
        cancel_link4.click()
        
        # logout and login again
        self.logout()
        self.login_user('mdco')

        # only item 1 must be complete
        checkbox1 = self.get_checkbox_for(1)
        self.assertTrue(checkbox1.is_selected())
        checkbox2 = self.get_checkbox_for(2)
        self.assertFalse(checkbox2.is_selected())
        checkbox3 = self.get_checkbox_for(3)
        self.assertFalse(checkbox3.is_selected())
        checkbox4 = self.get_checkbox_for(4)
        self.assertFalse(checkbox4.is_selected())

        # only item 3 must be disabled (cancelled)
        self.assertTrue(checkbox1.is_enabled())
        self.assertTrue(checkbox2.is_enabled())
        self.assertFalse(checkbox3.is_enabled())
        self.assertTrue(checkbox4.is_enabled())

