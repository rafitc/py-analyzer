import ast
from pathlib import Path
from typing import List

class PandasOptimizer():
    # list all allowd data read methods of pandas
    data_read_methods = ['read_csv', 'read_table', 'read_json', 'read_excel', 'read_sql', 'read_parquet', 'read_feather', \
                         'read_hdf', 'read_fwf', 'read_gbq', 'read_stata', 'read_sas', 'read_spss', 'read_orc']

    def __init__(self, module_path:str="", file_name:str="", is_file_path=True, code="") -> None:
        self.is_file_path = is_file_path
        # If the code is a file path, analyzer read entire file and convert into string
        if is_file_path:
            self.module_path = module_path
            self.file_name = file_name
            # Read full code as string
            self.code_as_text = Path(module_path).read_text()

        else: # if its not a filepath. then linter is expecting a valid python code in string format.
            self.code_as_text = code

        self.suggestions = []

    def is_valid_python(self):
        try:
            self.tree = ast.parse(self.code_as_text)
            return True
        except SyntaxError:
            self.give_suggestion(msg="There is a syntax error in your code. Analyzer is expecting valid python code")
            return False
    
    def give_suggestion(self, node:ast.Attribute=None, msg:str="") -> None:
        # this can be easily abstracted how ever we wanted based on the requirement 
        # for now, just pushing into list.
        # If issue from file add file name as well, else. don't include file name
        if node != None:
            if self.is_file_path:
                message = f"file: {self.file_name} | line no: {node.lineno} | {msg}"
                self.suggestions.append(message)

            else:
                message = f"line no: {node.lineno} | {msg}"
                self.suggestions.append(message)
        else:
            if self.is_file_path:
                msg = f"file: {self.file_name} | {msg}"
            self.suggestions.append(msg)
    
    def check_import(self) -> None:
        # its better to import pandas with namespace pd `import pandas as pd`
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                # Check is this related to pandas 
                for each_name in node.names:
                    if 'pandas' in each_name.name:
                        if each_name.asname != 'pd':
                            self.give_suggestion(node, "Use `pd` as namespace for python. eg: import pandas as pd")
    
    def check_data_read(self) -> None:
        # read keywords from data read ops
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                if hasattr(node.value.func, 'attr') and (node.value.func.attr in self.data_read_methods):
                    if 'dtype' not in [i.arg for i in node.value.keywords]:
                        self.give_suggestion(node, f"Use `dtype` with {node.value.func.attr} to reduce the memory usage.")
                    
                    if 'engine' not in [i.arg for i in node.value.keywords]:
                        self.give_suggestion(node, f"""Consider using the `pyarrow` engine for faster performance and multithreading support.
                                                    While the `python` engine is more feature-complete, the pyarrow engine can significantly
                                                    improve performance, especially for large datasets. """)
                        
                    if 'usecols' not in [i.arg for i in node.value.keywords]:
                        self.give_suggestion(node, "Load only necessary columns using the `usecols` parameter if you're dealing with large datasets and only need specific columns.")

    def check_iter(self) -> None:
        for node in ast.walk(self.tree):
            # check for for loop
            if isinstance(node, ast.For):
                # ensure the iterable is calling a method and that's is iterrows()
                if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Attribute):
                    if node.iter.func.attr == 'iterrows':
                        self.give_suggestion(node, "Found loop with `iterrows()`. Replace iterrows() with itertuples() for better performance.")
                    # full vectorization is completely depends on the bussines logic. 
                    if node.iter.func.attr == 'itertuples':
                        self.give_suggestion(node, "Try to use vectorization if possible instead of itertuples() else use apply()")
    
    def merge_statement(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                if hasattr(node.value, 'func') and hasattr(node.value.func, 'attr') and node.value.func.attr == 'merge':
                    if node.value.func.attr == 'merge':
                        # check for the keywords 
                        if 'on' not in [i.arg for i in node.value.keywords] and 'left_on' not in [i.arg for i in node.value.keywords] and 'right_on' not in [i.arg for i in node.value.keywords]:
                            self.give_suggestion(node, "Use merge() with the `on` parameter instead of relying on join() for better performance")
                        
                        if 'how' not in [i.arg for i in node.value.keywords]:
                            self.give_suggestion(node, "Use merge() with the `how` parameter instead of default value for better readability")
        
    def run(self) -> List[str]:
        # this are the methods, 
        # TODO Modularize the code by building child class for each methods
        if self.is_valid_python():
            self.check_import()
            self.check_data_read()
            self.check_iter()
            self.merge_statement()

        # Return all collected suggestions
        return self.suggestions


