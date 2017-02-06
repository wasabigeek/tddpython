from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # wasabi opens superlists in his browser
        self.browser.get(self.server_url)

        # he notices the page title and header mention Superlists
        self.assertIn('Superlists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start a new To-Do list', header_text)

        # he is able to enter a to-do item immediately
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # he types "Buy Lego Fairground Mixer" into a text box
        inputbox.send_keys('Buy Lego Fairground Mixer')

        # When he hits enter, he is taken to a new URL,
        # and now the page lists "1: Buy Lego Fairground Mixer" as a to-do
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Lego Fairground Mixer')

        # There is still a text box to input another item
        # He enters "Build Lego Fairground Mixer"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Build Lego Fairground Mixer')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and shows both to-dos
        self.wait_for_row_in_list_table('1: Buy Lego Fairground Mixer')
        self.wait_for_row_in_list_table('2: Build Lego Fairground Mixer')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # wasabi starts a new to-do list
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy Lego Fairground Mixer')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Lego Fairground Mixer')

        # he notices his list has a unique URL
        wasabi_list_url = self.browser.current_url
        self.assertRegex(wasabi_list_url, '/lists/.+')

        ## We use a new browser session to make sure no information
        ## of Wasabi's is coming though from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path=self.firefox_path
        ))

        # Now a new user, Rach, visits the home page. Wasabi's list is not there
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Lego Fairground Mixer', page_text)
        self.assertNotIn('Build Lego Fairground Mixer', page_text)

        # Rach creates a new list item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Rach gets her own unique URL
        rach_list_url = self.browser.current_url
        self.assertRegex(rach_list_url, '/lists/.+')
        self.assertNotEqual(rach_list_url, wasabi_list_url)

        # Again, there is no trace of wasabi's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Lego Fairground Mixer', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go to sleep