from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from todo.models import Item

class NewVisitorTest(StaticLiveServerTestCase):
    reset_sequences = True

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)
        self.browser.set_page_load_timeout(10)
        self.browser.get(self.live_server_url)
        sleep(0.5)

    def tearDown(self):
        self.browser.quit()

    def get(self, address):
        self.browser.get(self.live_server_url + address)

    def login_user(self, username, password='password'):
        self.send_keys_to_element_with_id(username, 'username')
        self.send_keys_to_element_with_id(password+'\n', 'password')

    def logout(self):
        logout_link = self.browser.find_element_by_id('logout')
        logout_link.click()

    def send_keys_to_element_with_id(self, keys, element_id):
        element = self.browser.find_element_by_id(element_id)
        for key in keys:
            sleep(0.15)
            element.send_keys(key)

    def input_new_item(self, text):
        self.send_keys_to_element_with_id(text + '\n', 'new_item_text')

    def check_for_item_in_item_list(self, item_text):
        item_list = self.browser.find_element_by_id('item_list')
        items = item_list.find_elements_by_class_name('item_text')
        self.assertIn(item_text, [item.text for item in items])

    def get_id_for_item_with_text(self, item_text):
        item = Item.objects.get(text=item_text)
        return item.id

    def get_checkbox_for(self, item_text):
        sleep(1)
        item_id = self.get_id_for_item_with_text(item_text)
        item_checkbox = self.browser.find_element_by_id('checkbox-' + str(item_id))
        return item_checkbox

    def get_item_row(self, item_text):
        sleep(1)
        item_id = self.get_id_for_item_with_text(item_text)
        item_row = self.browser.find_element_by_id('item-' + str(item_id))
        return item_row

    def get_reschedule_link_for(self, item_text):
        item_row = self.get_item_row(item_text)
        dropdown = item_row.find_elements_by_class_name('dropdown-toggle')
        dropdown[0].click()
        reschedule_link = item_row.find_elements_by_class_name('reschedule_link')
        return reschedule_link[0]

    def get_cancel_link_for(self, item_text):
        item_row = self.get_item_row(item_text)
        dropdown = item_row.find_elements_by_class_name('dropdown-toggle')
        dropdown[0].click()
        cancel_link = item_row.find_elements_by_class_name('cancel_link')
        return cancel_link[0]

    
    def test_can_start_a_list_and_retrieve_it_later(self):
        mdco_items = ['Buy', 'Email']

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
        
        spfestin_item = 'Check'
        self.input_new_item(spfestin_item)

        # list from mdco must still not be viewable, but spfestin's is
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(mdco_items[0], page_text)
        self.assertNotIn(mdco_items[1], page_text)
        self.assertIn(spfestin_item, page_text)


    
    # preserve completed and cancelled states
    def test_can_change_item_attributes_and_retrieve_it_later(self):
        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        mdco_items = ['Type', 'Email', 'Call', 'Buy']
        for item in mdco_items:
            self.input_new_item(item)

        # check item 1 as complete
        checkbox1 = self.get_checkbox_for(mdco_items[0])
        checkbox1.click()
        # check item 2 as complete and then uncheck it
        checkbox2 = self.get_checkbox_for(mdco_items[1])
        checkbox2.click()
        checkbox2 = self.get_checkbox_for(mdco_items[1])
        checkbox2.click()
        # mark item 3 as cancelled
        cancel_link3 = self.get_cancel_link_for(mdco_items[2])
        cancel_link3.click()
        # mark item 4 as cancelled and then unmark it
        cancel_link4 = self.get_cancel_link_for(mdco_items[3])
        cancel_link4.click()
        cancel_link4 = self.get_cancel_link_for(mdco_items[3])
        cancel_link4.click()
        
        # logout and login again
        self.logout()
        self.login_user('mdco')

        checkbox1 = self.get_checkbox_for(mdco_items[0])
        checkbox2 = self.get_checkbox_for(mdco_items[1])
        checkbox3 = self.get_checkbox_for(mdco_items[2])
        checkbox4 = self.get_checkbox_for(mdco_items[3])

        # only item 1 must be complete        
        self.assertTrue(checkbox1.is_selected())
        self.assertFalse(checkbox2.is_selected())
        self.assertFalse(checkbox3.is_selected())
        self.assertFalse(checkbox4.is_selected())

        # only item 3 must be disabled (cancelled)
        self.assertTrue(checkbox1.is_enabled())
        self.assertTrue(checkbox2.is_enabled())
        self.assertFalse(checkbox3.is_enabled())
        self.assertTrue(checkbox4.is_enabled())

    
    def test_can_signup_and_login_later(self):
        self.get('/signup/')
        self.send_keys_to_element_with_id('mdco', 'username')
        self.send_keys_to_element_with_id('email', 'email')
        self.send_keys_to_element_with_id('pass', 'password1')
        self.send_keys_to_element_with_id('pass', 'password2')
        self.send_keys_to_element_with_id('Matthew', 'first_name')
        self.send_keys_to_element_with_id('Co', 'last_name')
        submit_btn = self.browser.find_element_by_id('submit_btn')
        submit_btn.click()
        sleep(3)
        
        self.get('/login/')
        self.login_user('mdco', 'pass')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome', page_text)

    def test_can_reschedule_item(self):
        User.objects.create_user(username='mdco', password='password', first_name='Matthew')
        self.login_user('mdco')
        self.input_new_item('Buy')
        reschedule_link = self.get_reschedule_link_for('Buy')
        reschedule_link.click()
        self.browser.find_element_by_id('date_dialog_datepicker').clear()
        self.send_keys_to_element_with_id('Jan. 1, 2000\n\n', 'date_dialog_datepicker')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overdue', page_text)
