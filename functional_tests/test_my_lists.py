from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        # Create logged in user
        email = 'tddpython@yahoo.com'
        self.create_pre_authenticated_session(email)

        # User goes to home page and starts a list
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Reticulate splines')
        list_page.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # she notices a "My Lists" link, for the first time
        my_lists_page = MyListsPage(self).go_to_my_lists_page()

        # she sees her list is in there, named according to it's first list item
        self.wait_for(lambda: self.browser.find_element_by_link_text('Reticulate splines'))
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        list_page.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under 'my lists', her new list appears
        my_lists_page.go_to_my_lists_page()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # She logs out. The 'My lists' option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))

