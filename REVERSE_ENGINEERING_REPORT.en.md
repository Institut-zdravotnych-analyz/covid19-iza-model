# Reverse Engineering / Audit — covid19-iza-model

## Scope
- **Repository:** https://github.com/Institut-zdravotnych-analyz/covid19-iza-model
- **Base:** `9e62ba6` (branch `main`), local clone `C:\Users\User\audit-repos\covid19-iza-model`.
- **Mode:** Phase 1 static audit (inspection/reading only, no simulations executed); Phase 2 correct/document and publish, with explicit user authorization.
- **Limitations:** no `numpy/pandas/scipy/numexpr/matplotlib/openpyxl/xlrd/pyxlsb` in environment; **Julia not installed**. No simulations/benchmarks/numerical reproduction executed. `python -m py_compile` passed on `model.py`, `help_functions.py` and `tests/test_path_safety.py`.

## Phase 1 — General Diagnosis
- **Architecture:** agent-based epidemiological model (COVID-19, Slovakia) with components: demographic/age/district initialization, vaccination, resistance/immunity, daily infection, "automat" (levels/restrictions), logging and plots.
- **Technologies:** Python, `numpy`, `pandas`, `matplotlib`, `scipy.interpolate`, `numexpr`, `cProfile`, `winsound` (Windows), `olefile`/Excel engines.
- **Maintenance:** research/operational snapshot (2021 dates/comments, hardcoded paths, commented blocks). Minimal README. No `requirements.txt`, CI or tests.
- **Public:** 0 Issues and 0 PRs listed on GitHub (current state).

## Problems investigated (REA IDs)
| ID | Sev | Status | Location | Summary |
|---|---|---|---|---|
| REA-001 | P1 | CONFIRMED | `model.py` `__main__`/`full_sim` | Non-reproducible/unsafe execution: hardcoded paths (`C:\Users\klukaa\...`), `winsound` (Windows-only), `break` after 1 scenario, `exit()` in branches, `plt.show`, `pd.to_datetime("today")`. |
| REA-002 | P1 | CONFIRMED | `model.py:424` | Global `np.random.seed(1)` and RNG not injected; global state leaks between runs/tests. |
| REA-003 | P1 | PROBABLE | `model.py:112, 222, 223, 266+` | Divisions by `protection_delay`, `test_ratio`, `len(df)`, `spolu` without zero guard → `inf/NaN` or `ZeroDivisionError` with extreme parameters. |
| REA-004 | P2 | CONFIRMED | `model.py:179-180` | `np.random.geometric(1/(R0/infectious_l[j]+1), n)` may be invalid with extreme/negative `R0`. |
| REA-005 | P2 | CONFIRMED | `help_functions.py:21-36` | `save_df` silently overwrites (`os.remove`); unknown extensions only print. |
| REA-006 | P2 | CONFIRMED | `model.py:26-27` | Decorator `profile` writes `profile.txt` to cwd (side effect). |
| REA-007 | P2 | CONFIRMED | `model.py:10,1047`; `help_functions.py` | `winsound` breaks on Linux/macOS; Excel reading depends on optional engines without clear verification. |
| REA-008 | P2 | CONFIRMED | `help_functions.py:415` | Path logic assumes Windows separator `\` in some places; fragile portability. |
| REA-009 | P2 | PROBABLE | `model.py` automat/`novy_automat` | Deprecated `DataFrame.append` in loops and fixed time windows; short data may produce empty/NaN slices. |
| REA-010 | P2 | CONFIRMED | `params_data/~$*.xlsx` | Excel temporary files tracked in repo; confusion risk. |
| REA-011 | P3 | CONFIRMED | Repository | No deps declared, lock, tests, CI, insufficient README. |
| REA-012 | P3 | CONFIRMED | `model.py`/`help_functions.py` | Commented blocks, prints, `if False`, magic constants, `exit()`/"lazy function is broken" checks. |

## Recurring problems
None documented publicly (0 Issues/PRs). Not invented.

## Implemented changes (Phase 2)
1. **`.gitignore` (new)**: ignores `__pycache__/`, `*.py[cod]`, `.venv/`, `profile.txt`, `*.log`, `~$*.xlsx`, `~$*.xls`, `*.ipynb_checkpoints/`, `.DS_Store`, `Thumbs.db`. **Does not ignore tracked input data** (CSV/XLSX of the repo).
2. **`README.md` expanded**: scope/safety, dependencies, how to run, portability limits (Windows/hardcoded paths), reproducibility and suggested best practices.
3. **`tests/test_path_safety.py` (new)**: pure-Python tests (no deps) validating that `os.path.join` does not escape the base directory and that `~$*.xlsx` locks are recognized.
4. `help_functions.py`: **not changed** (restored to HEAD) to avoid scientific regression without numerical validation.
5. `model.py`: **not changed** (restored to HEAD) to avoid scientific regression without numerical validation.

## Changes NOT implemented (need numerical validation/regression)
- Extreme parameter validation (REA-003/004): requires fixed-seed tests and controlled dataset before/after.
- Injected RNG / `default_rng` (REA-002): may change stochastic results if RNG order changes.
- CLI/importable entrypoint, `winsound`/profile guard (REA-001/006/007): safe, but out of the minimum scope approved in this round.

## Validation performed
- `python -m py_compile model.py help_functions.py tests/test_path_safety.py` → OK.
- `python tests/test_path_safety.py` → OK.
- Not executed: full simulation, benchmarks, numerical regression (deps/runtime data unavailable).

## Remaining risks
- Scientific results depend on seed and RNG order; RNG changes require regression.
- Hardcoded paths and `winsound` limit execution outside the original author's environment.
- No regression tests with real data.
