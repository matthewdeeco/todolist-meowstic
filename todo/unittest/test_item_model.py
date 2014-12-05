from django.test import TestCase
from todo.models import Item

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'item 1'
        first_item.save()

        second_item = Item()
        second_item.text = 'item 2'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'item 1')
        self.assertEqual(second_saved_item.text, 'item 2')