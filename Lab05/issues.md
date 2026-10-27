# Lab 5 – Identified Issues: `supplier_orders.py`

Line numbers refer to the **original** file (before any fixes). Reports are in
`reports/before/` (original code) and `reports/after/` (fixed code).

## Summary

| Tool   | Before                         | After            |
|--------|--------------------------------|------------------|
| Pylint | 2.41/10 (22 messages)          | **10.00/10**     |
| Bandit | 3 issues (1 High, 1 Medium, 1 Low) | **0 issues** |
| Flake8 | 4 issues                       | **0 issues**     |

## Issue table (high and medium severity first)

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Shell command injection | Security (High) | Bandit B605 | 21 | `os.system("echo ... " + supplier)` runs a shell command built from the supplier name. A name like `Acme; rm -rf ~` would run arbitrary commands. | Removed the shell call entirely and used `print()` to send the notification. Removed the now-unused `import os`. |
| 2 | SQL injection | Security (Medium) | Bandit B608, Pylint C0209 | 11 | The `INSERT` query was built with `%` string formatting, so a supplier or item containing `'` breaks the query or injects SQL. | Switched to a parameterised query with `?` placeholders and passed the values as a tuple to `execute()`. |
| 3 | Mutable global state | Bug / Design | Pylint W0603, C0103 | 6, 10, 12 | `order_total` was a module-level global changed with `global` inside `placeOrder`, so the total silently accumulated across calls and was hard to test. | Removed the global. `place_order()` now returns the quantity and `main()` keeps the total in a local variable. |
| 4 | Database connection created at import | Bug / Design | Pylint W0621 (×4) | 4–5, 9, 16, 24, 31 | The connection `conn` was created at module level and every function shadowed it with a parameter of the same name, which is confusing and error-prone. The connection was also never closed. | Moved setup into a `create_database()` function, renamed the parameter to `connection`, and close the connection at the end of `main()`. |
| 5 | Broad exception silently swallowed | Bug / Security (Low) | Bandit B110, Pylint W0718 | 25–28 | `except Exception: pass` hides every error in `cleanup()`, including programming mistakes, so failures go unnoticed. | Catch only `sqlite3.Error` and report the error message instead of ignoring it. |
| 6 | Unused argument | Bug | Pylint W0613 | 16 | `markReceived()` accepted `remarks` but never stored it, so the caller's remarks were silently lost. | Added a `remarks` column to the table and stored it in the `UPDATE` query. |
| 7 | Code runs on import | Bug / Design | (found in review) | 44 | `main()` was called unconditionally, so importing the module (e.g. for tests) would run the demo. | Wrapped the call in `if __name__ == "__main__":`. |
| 8 | Non-PEP 8 function names | Style | Pylint C0103 (×4) | 9, 16, 20, 31 | `placeOrder`, `markReceived`, `notifyWarehouse`, `pendingCount` use camelCase. | Renamed to `place_order`, `mark_received`, `notify_warehouse`, `pending_count`. |
| 9 | Missing docstrings | Style | Pylint C0114, C0116 (×6) | 1, 9, 16, 20, 24, 31, 35 | No module or function docstrings. | Added a module docstring and a one-line docstring to every function. |
| 10 | Lines too long | Style | Flake8 E501, Pylint C0301 | 5, 11, 32 | Lines of 122, 131 and 87 characters (limit 79 for Flake8, 100 for Pylint). | Split the SQL strings across lines using implicit string concatenation and wrapped the `execute()` calls. |
| 11 | Missing whitespace around operator | Style | Flake8 E225 | 12 | `order_total+=quantity` | Changed to `order_total += ...`. |

## Commits

1. `Add baseline Pylint, Bandit and Flake8 reports (before fixes)`
2. `Fix Bandit issues` – issues 1, 2, 5
3. `Fix Pylint issues` – issues 3, 4, 6, 7, 8, 9
4. `Fix Flake8 issues` – issues 10, 11

The program still behaves the same: it prints `notifying warehouse about Acme`
followed by `1 540` (1 pending order, 540 items ordered in total).
