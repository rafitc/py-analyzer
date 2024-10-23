# Optimize your data science code base.

A code monitoring tool to help you optimize your data science-related source code.

## Requirements

- Python 3.11.3

# Problem

Python is a widely used programming language for handling data-intensive operations. Libraries like [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/) are commonly used for such tasks, as they are optimized for heavy computation. Their underlying C code, vectorization, and the use of ndarray structures make them very fast.

However, even with these optimizations, developers often write less efficient code by not adhering to the best practices of pandas and NumPy. For example, using `iterrows()` instead of `itertuples()` can slow down data processing.

**Py-Analyzer** is a tool designed to identify such inefficiencies in your code and provide better suggestions for optimization. Simply provide the path to your source code, and Py-Analyzer will offer recommendations to improve its performance.

## Reference

These are few good reference for you to follow best coding standard.

- https://pandas.pydata.org/docs/user_guide/enhancingperf.html
- https://medium.com/bigdatarepublic/advanced-pandas-optimize-speed-and-memory-a654b53be6c2
- https://numpy.org/devdocs/user/basics.html
- https://blog.paperspace.com/numpy-optimization-vectorization-and-broadcasting/
- https://ryxcommar.com/2020/01/15/for-the-love-of-god-stop-using-iterrows/
