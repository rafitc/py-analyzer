# Py-Analyzer

Optimize your data intensive operations

# Problem

Python is a widely used programming language for handling data-intensive operations. Libraries like [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/) are commonly used for such tasks, as they are optimized for heavy computation. Their underlying C code, vectorization, and the use of ndarray structures make them very fast.

However, even with these optimizations, developers often write less efficient code by not adhering to the best practices of pandas and NumPy. For example, using `iterrows()` instead of `itertuples()` can slow down data processing.

**Py-Analyzer** is a tool designed to identify such inefficiencies in your code and provide better suggestions for optimization. Simply provide the path to your source code, and Py-Analyzer will offer recommendations to improve its performance.

# Analyzer rules

[Refer Here](docs/README.md) for the rules and pattern

## Requirements

- Python 3.11.3
- numpy==2.1.2
- pandas==2.2.3
- python-dateutil==2.9.0.post0
- pytz==2024.2
- six==1.16.0
- tzdata==2024.2

## How to run the analyzer

1. Clone the code `git clone https://github.com/rafitc/py-analyzer`
2. Go to the project folder `cd py-analyzer`
3. Create python virtual env with `python 3.11` as base
4. Activate virtual env
5. Install the dependencies `pip install -r requirements.txt`
6. Run the analyzer by providing python project directory. `python src/main.py <PROVIDE-YOUR-PYTHON-PROJECT-DIRECTORY>`
   1. Eg:- `python src/main.py test/test_files`

## How to run the unit tests (for developers)

1. Clone the code `git clone https://github.com/rafitc/py-analyzer`
2. Go to the project folder `cd py-analyzer`
3. Create python virtual env with `python 3.11` as base
4. Activate virtual env
5. Install the dependencies `pip install -r requirements.txt`
6. Run the test suite along your code `python -m unittest test/test_analyzer.py`

## Future tasks

Currently the tool only support few operations from `pandas` library. Eventually this will support other data intensive libraries `numpy`, `matplotlib` `SciPy` etc.

Code modularization is needed in `PandasOptimizer` as it grow, there will be many child classes each classes will take care each subcategory of rules.

Logger implementation is pending

# TODO

- [x] Read files from given root directory
- [x] Parse each files and check for valid python code base
- [x] Support both file and direct code as input for the analyzer class
- [x] Implement first rule check with test cases
- [x] Implement multiple rule check with test cases
- [x] Populate suggestions with line no and file name
- [ ] Modularize the `PandasOptimizer` class methods into child classes
- [ ] Implement controllable loggers
- [ ] Finish all the rules of pandas
- [ ] Write rules for other libraries like `numpy`, `SciPy` etc
