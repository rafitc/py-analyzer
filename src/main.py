import sys
import os

from pyanalyzer.analyze import PandasOptimizer

def main():

    # First get the file path from sys argument 
    if not len(sys.argv) > 1:
        print("File name is not passed. Provide your source code path ton validate.")
        exit(0)
    
    project_path = sys.argv[1]
    print("Got project path ", project_path)

    # then look for python modules in all hierarchy structure
    # for example just take main.py 
    for root, dirs, files in os.walk(project_path):
        # get each full file path
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                check = PandasOptimizer(file_path, file)
                check.run()

if __name__ == '__main__':
    main()