<div align="center">
  <img src="https://raw.githubusercontent.com/Khader-X/logo/refs/heads/main/logo-2-1.png" alt="[Project Name] Logo" width="200"/>
</div>

# Releasing

This document outlines the steps to release a new version of the project.

## Prerequisites

- Ensure all tests pass
- Update version in `__version__.py`
- Update `CHANGELOG.md` with the new changes
- Commit all changes

## Steps

1. Create a new tag for the release:
   ```
   git tag v1.0.0
   ```

2. Push the tag to the repository:
   ```
   git push origin main --tags
   ```

3. If publishing to PyPI:
   - Build the package: `python -m build`
   - Upload: `twine upload dist/*`

4. Create a GitHub release if applicable, copying the changelog entry.

## Versioning

This project uses [Semantic Versioning](https://semver.org/).
