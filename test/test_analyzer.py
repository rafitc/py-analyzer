import unittest
from pyanalyzer.PandasOptimizer import PandasOptimizer

class PandasOptimizeTest(unittest.TestCase):
    
    def test_valid_python_code(self):
        code = """some random strings"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ["There is a syntax error in your code. Analyzer is expecting valid python code"])
    
    def test_pandas_invalid_import(self):
        code = """import pandas"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), [])

    def test_pandas_valid_import(self):
        code = """import pandas as pd"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), [])

if __name__ == '__main__':
    unittest.main()