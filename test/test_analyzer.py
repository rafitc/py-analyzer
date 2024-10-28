import unittest
from pyanalyzer.PandasOptimizer import PandasOptimizer

class PandasOptimizeTest(unittest.TestCase):
    
    def test_invalid_python_code(self):
        code = """some random strings"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ["There is a syntax error in your code. Analyzer is expecting valid python code"])
    
    def test_valid_python_code(self):
        code = """ print("hello world") """
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ["There is a syntax error in your code. Analyzer is expecting valid python code"])
    
    def test_pandas_invalid_import(self):
        code = """import pandas"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ['line no: 1 | Use `pd` as namespace for python. eg: import pandas as pd'])

    def test_pandas_valid_import(self):
        code = """import pandas as pd"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), [])
    
    def test_pandas_valid_dataread(self):
        code = """import pandas as pd
df = pd.read_csv("data.csv", dtype={'a': np.float64, 'b': np.int32, 'c': 'Int64'}, usecols=['a', 'b', 'c'], engine='pyarrrow')"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), [])
    
    def test_pandas_invalid_dataread(self):
        code = """import pandas as pd
df = pd.read_csv("data.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ['line no: 2 | Use `dtype` with read_csv to reduce the memory usage.'])

    def test_pandas_invalid_loop(self):
        code = """import pandas as pd
df = pd.read_csv("data.csv", dtype={'a': np.float64, 'b': np.int32, 'c': 'Int64'}, usecols=['a', 'b', 'c'], engine='pyarrrow')
for row in df.iterrows():
    pass"""
        test_obj = PandasOptimizer(is_file_path=False, code=code)
        self.assertEqual(test_obj.run(), ['line no: 3 | Found loop with `iterrows()`. Replace iterrows() with itertuples() for better performance.'])

    def test_pandas_invalid_loop(self):
            code = """import pandas as pd
df = pd.read_csv("data.csv", dtype={'a': np.float64, 'b': np.int32, 'c': 'Int64'}, usecols=['a', 'b', 'c'], engine='pyarrrow')
for row in df.itertuples():
        pass"""
            test_obj = PandasOptimizer(is_file_path=False, code=code)
            self.assertEqual(test_obj.run(), ['line no: 3 | Try to use vectorization if possible instead of itertuples() else use apply()'])

    def test_pandas_invalid_merge(self):
        code = """import pandas as pd
df = pd.merge(df1, df2)"""
        test_obj = PandasOptimizer(is_file_path=False, code=code) 
        self.assertEqual(test_obj.run(), ['line no: 2 | Use merge() with the `on` parameter instead of relying on join() for better performance',
                                          'line no: 2 | Use merge() with the `how` parameter instead of default value for better readability'])
        
    def test_pandas_invalid_merge(self):
        code = """import pandas as pd
df = pd.merge(df1, df2, how='left', left_on='col_1')"""
        test_obj = PandasOptimizer(is_file_path=False, code=code) 
        self.assertEqual(test_obj.run(), [])
        
if __name__ == '__main__':
    unittest.main()