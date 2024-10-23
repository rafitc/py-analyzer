import ast

class IterrowsChecker(ast.NodeVisitor):
    def __init__(self):
        self.iterrows_found = False

    def visit_Call(self, node):
        # Check if the call is a method call using iterrows()
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "iterrows":
                self.iterrows_found = True
                print(f"Usage of iterrows() found on line {node.lineno}")
        
        # Recursively visit all child nodes
        self.generic_visit(node)

def check_iterrows_usage(code):
    tree = ast.parse(code)
    checker = IterrowsChecker()
    print("checker :", checker)
    checker.visit(tree)
    if not checker.iterrows_found:
        print("No usage of iterrows() found. Consider using itertuples() for better performance.")

# Example usage:
code_to_check = """
import pandas as pd

df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

# This will trigger the warning
for index, row in df.itertuples():
    print(row['A'], row['B'])
"""

check_iterrows_usage(code_to_check)
