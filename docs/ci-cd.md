<!-- https://docs.streamlit.io/develop/concepts/app-testing/automate-tests -->

#### Automation
- **CI Tools**: Use tools like GitHub Actions, Jenkins, or GitLab CI.
- **GitHub Actions**: Create a `.github/workflows/main.yml` file. Use the Streamlit App Action to set up Python, install dependencies, and run smoke tests for `app.py` and `pages/`. Add `pytest` for custom tests.
- **Smoke Tests**: The Streamlit App Action checks if the app runs without crashing.
- **Enhanced Reporting**: Integrate `pytest-results-action` for JUnit XML output.
- **Customization**: Tailor workflows for linting, security scans, or advanced tests.
