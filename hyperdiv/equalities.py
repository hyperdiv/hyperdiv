equalities = dict()


def register_equality(typ, fn):
    """
    Hyperdiv determines if prop values changed by doing `bool(old_value
    != new_value)`. Some types override `!= (`__ne__`) to return
    non-bool-like values, causing `bool(old_value != new_value) to fail.

    Using `register_equality`, you can define a custom equality
    function. The equality function takes two values of a given type
    and returns `True` if the values are equal and `False` otherwise.

    For example, Hyperdiv automatically adds a custom equality
    function for `pandas.DataFrame`, like this:

    ```py-nodemo
    hd.register_equality(pandas.DataFrame, lambda df1, df2: df1.equals(df2))
    ```
    """
    equalities[typ] = fn


try:
    from pandas import DataFrame

    register_equality(DataFrame, lambda df1, df2: df1.equals(df2))
except Exception:
    pass
