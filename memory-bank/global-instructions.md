This is a python project. We use types everywhere we can and have a strict type checker.

### Typing lists
One  of the easier linting errors to solve is when we create a list without a type. Example:
```python
new_list = []
new_list.append("item") # the linter will complain that the type is unknown
```
To fix this, we need to specify the type of the list when we create it:
```python
new_list: list[str] = []
new_list.append("item") # now the linter is happy
```

### Ignoring st.* methods
We use streamlit for our UI. Streamlit has poor typing support, so generally, we ignore linting errors for methods such as st.write by using `# type: ignore` at the end of the line. Example:
```python
st.write("Hello, world!")  # type: ignore
```
