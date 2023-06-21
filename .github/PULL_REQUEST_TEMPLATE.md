### Describe PR

<!--

Simply describe what have you done, and also if your PR resolves an issue please link it here.

-->

Before submitting your PR, please review the following checklist:

<!--

write 'x' inside the box if you want to select it, e.g. [x],
or simply select it box with your mouse after you finishing
all other sections.

-->

- [ ] **DO** keep pull request small so it can be easily reviewed.
- [ ] **DO** make sure that the code is runnable.
- [ ] **DO** make sure that the code pass **ALL** linter/tests:

  1. `pylint $(git ls-files '*.py') --py-version=3.10 --ignore="build,__init__.py" --disable=useless-suppression`
  2. `mypy . --exclude build --exclude __init__.py --ignore-missing-imports`
  3. `pytest`

  ```shell
  pylint $(git ls-files '*.py') --py-version=3.10 --ignore="build,__init__.py" --disable=useless-suppression; mypy . --exclude build --exclude __init__.py --ignore-missing-imports; pytest
  ```

- [ ] **DO** make sure that `setup.py` has already been updated with new dependencies and version changing.
- [ ] **DO** make sure that `README.MD` has already been updated with related infos.
- [ ] **AVOID** contain any password, abs file path, ip-address, etc.
