<!-- https://docs.streamlit.io/develop/concepts/app-testing -->
<!-- https://docs.streamlit.io/develop/concepts/app-testing/get-started -->
<!-- https://docs.streamlit.io/develop/concepts/app-testing/beyond-the-basics -->
<!-- https://docs.streamlit.io/develop/concepts/app-testing/automate-tests -->

### Testing Streamlit Applications: A Concise Guide

#### Getting Started
- **Core Tools**: Use `streamlit.testing.v1` to test Streamlit apps programmatically. Use `pytest` to run and manage tests.
- **Project Structure**: Place your Streamlit app (e.g., `app.py`) in the root directory. Put test files in a `tests/` subdirectory (e.g., `tests/test_app.py`).
- **Naming Conventions**: Test files must be named `test_<name>.py` or `<name>_test.py`. Test functions must start with `test_` (e.g., `test_increment`).

#### Basic Testing
- **Loading the App**: Use `AppTest.from_file("path/to/app.py")` to load your app into the test environment, then call `.run()` to simulate its initial execution.
- **Accessing UI Elements**: Retrieve elements via `AppTest` attributes (e.g., `at.button`, `at.number_input`). Use indices (e.g., `at.button[0]`) or keys (e.g., `at.button(key="submit")`) if defined. Access container elements like `at.sidebar.checkbox` or `at.columns[0].button` or `at.tabs[0].button`.
  - always prefer keys to indices.
- **Manipulating Widgets**: Set values with `.set_value()` (e.g., `at.slider[0].set_value(5)`). Use specific methods like `.click()` for buttons or `.increment()` for number inputs. Call `.run()` after each interaction to simulate a rerun.
- **Inspecting Elements**: Check values with `.value` (e.g., `at.text_input[0].value`). Other attributes like `label`, `options`, or `disabled` may be available depending on the element.
- **Assertions**: Use `assert` to verify behavior (e.g., `assert at.text[0].value == "Expected"`).

#### Running Tests
- **Using pytest**: Run `pytest` from the project root. It automatically discovers and executes all test files in `tests/` and test functions starting with `test_`.

#### Advanced Testing
- **Mutable Attributes**:
  - `AppTest.secrets`: Set secrets before `.run()` (e.g., `at.secrets["db_username"] = "Jane"`).
  - `AppTest.session_state`: Manipulate state (e.g., `at.session_state["key"] = "value"`).
  - `AppTest.query_params`: Set URL parameters (e.g., `at.query_params["id"] = "123"`).
- **Use Cases**: Test secrets handling, jump to specific states, or simulate multipage app transitions.

#### Conclusion
Use `streamlit.testing.v1` and `pytest` for structured testing.