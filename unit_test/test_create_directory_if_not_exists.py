import boston.main

import unittest
import os

class TestCreateDirectory(unittest.TestCase):
    
    path = "prueba"

    def test_that_when_input_not_string_then_raises_type_error(self):

        self.assertRaises(TypeError, boston.main.create_directory_if_not_exists, 2)

    def test_that_when_called_then_return_is_none(self):

        self.assertEqual(boston.main.create_directory_if_not_exists(self.path), None)


if __name__ == '__main__':
    unittest.main()

