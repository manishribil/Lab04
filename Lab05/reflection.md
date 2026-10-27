# Lab 5 – Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues from Flake8 and Pylint: renaming camelCase
functions to snake_case, adding docstrings, wrapping long lines and adding
spaces around `+=`. These are mechanical changes that don't affect how the
program behaves.

The hardest was removing the global `order_total`. It wasn't a one-line fix:
I had to change what `place_order()` returns and move the running total into
`main()`, then check that the program still printed the same result (`1 540`).
Moving the database connection out of module scope was similar, because every
function depended on it. The SQL injection fix was conceptually important but
easy once I knew to use `?` placeholders.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Not strictly, but some findings matter less in this context. Pylint's
`C0103` flagged `order_total` because module-level names are treated as
constants and should be `UPPER_CASE`. Renaming it would have silenced the
warning but not fixed the real problem, which was that it was mutable global
state. Similarly, Bandit's B608 is only rated "Medium" confidence because it
can't be sure the string is SQL with user input, and in this demo the inputs
are hard-coded. It was still worth fixing, since real supplier names would
come from users. Some tools also overlap: the long lines were reported by both
Flake8 (79 characters) and Pylint (100 characters) with different limits.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor so issues show up while
  typing, and use a `pre-commit` hook so code with Bandit or Flake8 errors
  can't be committed.
- **In CI:** add a GitHub Actions workflow that runs all three tools on every
  push and pull request, failing the build on any Bandit issue of Medium or
  High severity, any Flake8 error, or a Pylint score below a threshold (e.g. 9.5).
- **Configuration:** keep the settings in the repo (`.pylintrc`, `setup.cfg`
  or `pyproject.toml`) so the whole team uses the same rules, and use `# nosec`
  or Pylint disables only with a comment explaining why.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** the two real vulnerabilities (shell command injection and SQL
  injection) are gone. Bandit went from 3 issues to 0.
- **Robustness:** errors in `cleanup()` are no longer silently swallowed, the
  database connection is closed, and the `remarks` argument is actually saved
  instead of being thrown away.
- **Testability:** with no global state and no code running at import time,
  each function can be imported and tested on its own with a fresh database.
- **Readability:** consistent PEP 8 names, docstrings and short lines make the
  code easier to read. Pylint went from 2.41/10 to 10.00/10 and Flake8 from 4
  issues to 0, while the program's output stayed the same.
