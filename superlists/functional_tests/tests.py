from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            # using git bash on windows 
            firefox_path='C:/Program Files (x86)/Mozilla Firefox/firefox.exe'
        ))
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_later(self):
        # wasabi opens superlists in his browser
        self.browser.get(self.live_server_url)

        # he notices the page title and header mention Superlists
        self.assertIn('Superlists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Superlists', header_text)

        # he is able to enter a to-do item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a To-do'
        )

        # he types "Buy Lego Fairground Mixer" into a text box
        inputbox.send_keys('Buy Lego Fairground Mixer')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy Lego Fairground Mixer" as a to-do
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy Lego Fairground Mixer')

        # There is still a text box to input another item
        # He enters "Build Lego Fairground Mixer"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Build Lego Fairground Mixer')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and shows both to-dos
        self.check_for_row_in_list_table('1: Buy Lego Fairground Mixer')
        self.check_for_row_in_list_table('2: Build Lego Fairground Mixer')

        # Wasabi checks the page URL

        # He visits that URL and sees the to-do list is still there

        # He closes the browser

        self.fail('Finish the test!')
