import ast
from pathlib import Path

class PandasOptimizer(ast.NodeVisitor):
    # list all allowd data read methods of pandas
    data_read_methods = ['read_csv', 'read_table', 'read_json', 'read_excel', 'read_sql', 'read_parquet', 'read_feather', \
                         'read_hdf', 'read_fwf', 'read_gbq', 'read_stata', 'read_sas', 'read_spss', 'read_orc']

    def __init__(self, module_path:str, file_name:str) -> None:
        self.module_path = module_path
        self.file_name = file_name
        # Read full code as string
        code_as_text = Path(module_path).read_text()
        self.tree = ast.parse(code_as_text)
    
    def give_suggestion(self, node:ast.Attribute, msg:str):
        # for now, just using classical `print` statement. 
        # this can be easily abstracted how ever we wanted, example loggers
        print(f"Suggestion in file: {self.file_name} | line no: {node.lineno} | {msg}")
    
    def check_import(self):
        # its better to import pandas with namespace pd `import pandas as pd`
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                # Check is this related to pandas 
                for each_name in node.names:
                    if 'pandas' in each_name.name:
                        if each_name.asname != 'pd':
                            self.give_suggestion(node, "Use `pd` as namespace for python. eg: import pandas as pd")
    
    def check_data_read(self):
        # use given methods to 
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and (node.value.func.attr in self.data_read_methods):
                if 'dtype' not in [i.arg for i in node.value.keywords]:
                    self.give_suggestion(node, f"Use `dtype` with {node.value.func.attr} to reduce the memory usage.")
                
                if 'engine' not in [i.arg for i in node.value.keywords]:
                    self.give_suggestion(node, f"""Consider using the `pyarrow` engine for faster performance and multithreading support.
                                                While the `python` engine is more feature-complete, the pyarrow engine can significantly
                                                improve performance, especially for large datasets. """)
                    
                if 'usecols' not in [i.arg for i in node.value.keywords]:
                    self.give_suggestion(node, "Load only necessary columns using the `usecols` parameter if you're dealing with large datasets and only need specific columns.")

    
    
    def check_dataframe_variable_name(self):
        # check df at the end for all
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name):
                print("yes")
        pass

    def check_iter(self):
        for node in ast.walk(self.tree):
            # check for for loop
            if isinstance(node, ast.For):
                # ensure the iterable is calling a method and that's is iterrows()
                if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute):
                    if node.iter.func.attr == 'iterrows':
                        self.give_suggestion(node, "Found loop with `iterrows()`. Replace iterrows() with itertuples() for better performance.")
                    # if itertuple is there, suggest to use apply or vectorization. 
                    # full vectorization is completely depends on the bussines logic. 
                    if node.iter.func.attr == 'itertuples':
                        self.give_suggestion(node, "Try to use vectorization if possible instead of itertuples() else use apply()")
    
    def merge_statement(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                if node.value.func.attr == 'merge':
                    # check for the keywords 
                    if 'on' not in [i.arg for i in node.value.keywords]:
                        self.give_suggestion(node, "Use merge() with the `on` parameter instead of relying on join() for better performance")
                    
                    if 'how' not in [i.arg for i in node.value.keywords]:
                        self.give_suggestion(node, "Use merge() with the `how` parameter instead of default value for better readability")

    def run(self):
        self.check_data_read()
        self.check_import()
        self.check_iter()
        self.merge_statement()


