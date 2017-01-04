from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Wasabi goes to the home page and tries to submit an empty list item
        # He hits enter on the empty input box

        # The home page refreshes with an error saying list items cannot be blank

        # He tries again with some text for the item, which now works

        # He decides to submit another blank item

        # He receives a similar Warning

        # He corrects it by filling some text in
        self.fail('write me!')
