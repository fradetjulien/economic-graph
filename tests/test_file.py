import unittest
import sys
sys.path.append('../module')
from index import is_csv

class TestFile(unittest.TestCase):

    def test_wrong_csv_file(self):
        file = "../assets/data"
        result = is_csv(file)
        self.assertEqual(result, False)

    def test_real_csv_file(self):
        file = "../assets/data.csv"
        result = is_csv(file)
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
