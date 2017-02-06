from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


    def test_cannot_add_empty_list_items(self):
        # Wasabi goes to the home page and tries to submit an empty list item
        # He hits enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # HTML5 validation intercepts the request, and does not load the page
        self.assertNotIn(
            'Buy Milk',
            self.browser.find_element_by_tag_name('body').text
        )

        # He tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.wait_for_row_in_list_table('1: Buy milk')

        # He decides to submit another blank item
        self.get_item_input_box().send_keys('\n')

        # HTML5 validation intercepts the request, and does not load the page
        self.wait_for_row_in_list_table('1: Buy milk')
        rows = self.browser.find_elements_by_css_selector('#id_list_table tr')
        self.assertEqual(len(rows), 1)

        # He corrects it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')


    def test_cannot_add_duplicate_items(self):
        # Wasabi goes to home and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.wait_for_row_in_list_table('1: Buy wellies')

        # He accidentally tries to enter a duplicate
        self.get_item_input_box().send_keys('Buy wellies\n')

        # He sees a helpful error message
        self.wait_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # wasabi starts a list and causes a validation error
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Banter too thick\n')
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick\n')

        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # He types in the input box and the error clears
        self.get_item_input_box().send_keys('a')
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
