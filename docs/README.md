# Py Analyzer

Optimize your data intensive operations.

# Linter Rules Documentation

## Overview

Py Analyzer helps you to optimize your data intensive code bases by following best practices.

## Rules

### Rule 1: Import Check

- **Category**: Readability
- **Description**: To check the package import with proper namespace.
- **Why It's Important**: Using `import pandas as pd` is important because it follows a widely accepted community standard, making your code more consistent, readable, and accessible to others. This standardization helps avoid confusion, allows easier sharing of code snippets, and makes it simpler for others to understand and collaborate on your code, as most pandas documentation and tutorials use the `pd` alias
- **Example**:
  - **Bad**:
    ```python
    import pandas as data_science
    ```
  - **Good**:
    ```python
    import pandas as pd
    ```

### Rule 2: Data Read Check

- **Category**: Performance, Best Practice
- **Description**: To reduce the memory usage.
- **Why It's Important**: Using `usecols`, `dtype`, and `engine` in pandas read operations optimizes data loading by reducing memory usage and improving performance
- **Example**:

  - **Bad**:
    ```python
    import pandas as pd
    df = pd.read_csv("data.csv")
    ```
  - **Good**:

    ```python
    import pandas as pd
    df = pd.read_csv("data.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')

    ```

### Rule 3: Iter check

- **Category**: Performance
- **Description**: To reduce the memory usage and improve performance.
- **Why It's Important**: Using `itertuples()` over `iterrows()` in pandas is generally more efficient for iterating through DataFrame rows because, `iterrows()` is faster to access compared to the pandas Series objects returned by iterrows(). This results in better performance, especially with larger DataFrames.
- **Example**:

  - **Bad**:
    ```python
    import pandas as pd
    df = pd.read_csv("data.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    for row in df.iterrows():
        pass
    ```
  - **Good**:

    ```python
    import pandas as pd
    df = pd.read_csv("data.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    for row in df.itertuples():
        pass

    ```

### Rule 3: Merge check

- **Category**: Performance, Readability
- **Description**: To reduce the memory usage and improve performance.
- **Why It's Important**: Using the `on` and `how` keywords in `pd.merge()` allows for precise control over DataFrame merging.
- **Example**:

  - **Bad**:

    ```python
    import pandas as pd
    df1 = pd.read_csv("data_1.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    df2 = pd.read_csv("data_2.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    merged_df = pd.merge(df1, df2)
    ```

  - **Good**:

    ```python
    import pandas as pd
    df1 = pd.read_csv("data_1.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    df2 = pd.read_csv("data_2.csv", usecols=['a', 'b', 'c'], engine='pyarrrow')
    merged_df = pd.merge(df1, df2, how='left', left_on='col_1')
    ```

## Contributing

Contributions are welcome for new rules based on your experience and best practices.

## Reference

These are few good reference for you to follow best coding standard.

- https://pandas.pydata.org/docs/user_guide/enhancingperf.html
- https://medium.com/bigdatarepublic/advanced-pandas-optimize-speed-and-memory-a654b53be6c2
- https://numpy.org/devdocs/user/basics.html
- https://blog.paperspace.com/numpy-optimization-vectorization-and-broadcasting/
- https://ryxcommar.com/2020/01/15/for-the-love-of-god-stop-using-iterrows/
