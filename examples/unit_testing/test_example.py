import unittest


class ExampleTest(unittest.TestCase):

    def test_example_failure(self):
        self.assertEqual(1, 2)

    def test_example_pass(self):
        self.assertEqual(1, 1)
