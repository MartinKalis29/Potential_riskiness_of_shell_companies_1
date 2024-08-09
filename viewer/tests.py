from django.test import TestCase


class ExampleTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up data for all class methods.")

    def setUp(self):
        print("\nsetup: Run once for every test method to setup data.")

    def test_false(self):
        print("Test method: test_false")
        self.assertFalse(False)

    def test_add(self):
        print("Test method: test_add")
        result = 1 + 1
        self.assertEqual(result, 2)
