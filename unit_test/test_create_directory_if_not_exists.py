import boston.main

import unittest
import os

class TestCreateDirectory(unittest.TestCase):
    
    def test_creation(self):
        
        path = "prueba"

        if os.path.isdir(path):
            os.rmdir(path)

        boston.main.create_directory_if_not_exists(path)

        self.assertTrue(os.path.isdir(path))


if __name__ == '__main__':
    unittest.main()

