import boston.main

import unittest
import os

class TestCreateDirectory(unittest.TestCase):
    
    path = "prueba"

    def test_creation(self):
        

        if os.path.isdir(self.path):
            os.rmdir(self.path)

        boston.main.create_directory_if_not_exists(self.path)

        self.assertTrue(os.path.isdir(self.path))

    def test_return_none(self):

        self.assertEqual(boston.main.create_directory_if_not_exists(self.path), None)


if __name__ == '__main__':
    unittest.main()

