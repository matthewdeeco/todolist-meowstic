from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.browser.get(self.live_server_url)

    def login_user(self, username, password='password'):
        username_box = self.browser.find_element_by_id('username')
        username_box.send_keys(username)
        password_box = self.browser.find_element_by_id('password')
        password_box.send_keys(password)
        password_box.send_keys(Keys.ENTER)

    def tearDown(self):
        self.browser.quit()

    def check_for_item_in_item_list(self, item_text):
        table = self.browser.find_element_by_id('item_list')
        items = table.find_elements_by_class_name('item_text')
        self.assertIn(item_text, [item.text for item in items])

    def input_new_item(self, text):
        inputbox = self.browser.find_element_by_id('new_item_text')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        texts = ['item 1', 'item 2']

        User.objects.create_user(username='mdco', password='password', email='mdco@example.com')
        self.login_user('mdco')
        self.input_new_item(texts[0])
        self.check_for_item_in_item_list(texts[0])
        # check that user is assigned a personal list url
        list_url = self.browser.current_url
        ## self.assertRegex(list_url, '/lists/.+')

        # check that both items are visible in the page
        self.input_new_item(texts[1])
        self.browser.implicitly_wait(5)
        self.check_for_item_in_item_list(texts[0])
        self.check_for_item_in_item_list(texts[1])

        """
        # switch to user 2
        self.tearDown()
        self.setUp()
        # list from user 1 must not be viewable
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(texts[0], page_text)
        self.assertNotIn(texts[1], page_text)
        # list url must be different from user 1's
        text2 = 'send email'
        self.input_new_item(text2)
        list_url2 = self.browser.current_url
        self.assertRegex(list_url2, '/lists/.+')
        self.assertNotEqual(list_url, list_url2)
        # list from user 1 must still not be viewable, but user 2's is
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(texts[0], page_text)
        self.assertNotIn(texts[1], page_text)
        self.assertIn(text2, page_text)
        """