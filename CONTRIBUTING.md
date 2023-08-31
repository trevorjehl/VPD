# Contributing Guidelines

Thank you for your interest in contributing to our Python repository! This document provides guidelines to ensure smooth and efficient collaboration.

## Getting Started

1. **Fork the Repository:** Click on the 'Fork' button at the top-right corner of the repository page on GitHub. This will create a copy of the repository in your account.

2. **Clone Your Fork:** Navigate to your fork and then clone it to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
   ```

3. **Add Upstream Remote:** After cloning, navigate to the project directory and add the main repository as 'upstream':
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/REPOSITORY_NAME.git
   ```

## Making Changes

1. **Create a New Branch:** Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/my_new_feature
   ```

2. **Make Your Changes:** Make and test your changes in this branch.

3. **Commit Your Changes:** Once you're satisfied, commit them with a clear and descriptive message.

   ```bash
   git add .
   git commit -m "Add a brief description of the changes"
   ```

4. **Keep Your Fork Updated:** Regularly pull from the `upstream` to keep your repository up-to-date.
   ```bash
   git pull upstream main
   ```

5. **Push to Your Fork:** Push your changes to your fork on GitHub.
   ```bash
   git push origin feature/my_new_feature
   ```

## Submitting a Pull Request

1. **Go to Your Fork on GitHub:** Navigate to your GitHub repository and click on the "New pull request" button.

2. **Describe Your Changes:** In the pull request form, ensure you provide a clear description of what you did and why. If your pull request addresses an open issue, include a reference to it (e.g., `Fixes #123`).

3. **Wait for Review:** Someone will review your pull request and may request changes or provide feedback.

4. **Make Necessary Changes:** If changes are requested, make them in your branch and push them again. The pull request will automatically update.

5. **Pull Request Gets Merged:** If everything looks good, your pull request will be merged into the main repository.

## Code Style and Linting

- Please adhere to the PEP 8 coding standards for Python. This ensures a consistent code base and improves code readability.
  
- Use `black` to format and check your code for PEP 8 compliance.

## Testing

Ensure that you write tests for any new features or fixes you implement. Tests help maintain the stability of the project.

## Feedback and Questions

If you have questions or need feedback, feel free to open an issue in the repository or contact me at tjehl@stanford.edu

---

Thank you for contributing! Your efforts help make this project better for everyone.