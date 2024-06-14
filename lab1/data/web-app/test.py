# unit test python file
import unittest

class TestApp(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()