import unittest
from pyanalyzer.PandasOptimizer import PandasOptimizer

class PandasOptimizeTest(unittest.TestCase):
    
    def test_valid_python_code(self):
        code = """import pandas as pd"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), [])


if __name__ == '__main__':
    unittest.main()