from pyanalyzer.PandasOptimizer import PandasOptimizer

import sys
import os

def main():

    # First get the file path from sys argument 
    if not len(sys.argv) > 1:
        print("File name is not passed. Provide your source code path to validate.")
        exit(0)
    
    project_path = sys.argv[1]
    print("Project path ->", project_path)
    all_suggestions = []
    FOUND_FILE = False
    # then look for python modules in all hierarchy structure
    # for example just take main.py 
    for root, dirs, files in os.walk(project_path):
        # get each full file path
        for file in files:
            if file.endswith(".py"):
                FOUND_FILE = True
                file_path = os.path.join(root, file)
                check = PandasOptimizer(file_path, file)
                result = check.run()
                all_suggestions.extend(result)

    if not FOUND_FILE:
        print("There are no python files in the given project path")
    # For now using classical print statement, this can be abstracted easily
    for each_suggestion in all_suggestions:
        print(each_suggestion)

def main_str():
    code  = """import pandas"""
    check = PandasOptimizer(is_file_path=False, code=code)
    result = check.run()

    for each_suggestion in result:
        print(each_suggestion)
    
if __name__ == '__main__':
    main()
    # main_str()