import time
import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    # using git bash on windows
    firefox_path = 'C:/Program Files (x86)/Mozilla Firefox/firefox.exe'

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


    def setUp(self):
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
            firefox_path=self.firefox_path
        ))
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        # TO-DO - update this based on the new edition and reuse wait_for
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)


    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)
