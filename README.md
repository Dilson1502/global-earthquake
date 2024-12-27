A python app to detect nearest earthquakes based on your geolocation (pre release).

## Code Quality Tools

### Flake8

- **Purpose**: Flake8 is a linting tool that checks your Python code for style guide enforcement (PEP 8), programming errors, and complexity issues. It helps identify potential problems in your code before runtime.
- **Functionality**: It combines checks from several tools:
  - **PyFlakes**: Checks for logical errors in your code.
  - **pycodestyle**: Checks for compliance with PEP 8, the style guide for Python code.
  - **mccabe**: Checks for code complexity (cyclomatic complexity).
- **Usage**: It is often used in continuous integration (CI) pipelines and during development to maintain code quality.

### Black

- **Purpose**: Black is an opinionated code formatter for Python. It automatically reformats your code to adhere to a specific style, making your code look consistent and cleaner.
- **Functionality**: Unlike Flake8, which points out style issues, Black modifies your code in place to correct those issues according to its own style guide. It focuses on producing readable code with minimal configuration required from the user.
- **Usage**: Developers typically run Black on their codebase to reformat it consistently, making it easier to read and collaborate.

### Summary

- **Flake8**: A linting tool that checks for errors and style issues without changing the code.
- **Black**: A code formatter that automatically reformats code to make it consistent and adhere to its own style rules.

Both tools can be used together: Flake8 can help identify issues in your code, while Black can help ensure consistent formatting.
