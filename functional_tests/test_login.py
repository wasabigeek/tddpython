import re

from django.core import mail

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

TEST_EMAIL = "test@test.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # User goes to the superlists site and enters her email address
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(
                'Could not find url in email body\n{}'.format(email.body)
            )
        url = url_search.group(0)
        self.assertIn(self.server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)