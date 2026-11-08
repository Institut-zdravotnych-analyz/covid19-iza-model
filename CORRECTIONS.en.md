# Corrections — covid19-iza-model

Base: `Institut-zdravotnych-analyz/covid19-iza-model@9e62ba6` (main). User authorized implementation of all viable proposals.

## Implemented

1. **`.gitignore` (new)**
   - Ignores Python caches, `profile.txt`, `*.log`, temporary Excel locks (`~$*.xlsx`/`~$*.xls`), notebook checkpoints, `.DS_Store`, `Thumbs.db`.
   - **Does not ignore** tracked input files (CSV/XLSX of the repo).

2. **`README.md` (updated)**
   - Scope and safety (research, not clinical product; technical review required).
   - Dependencies, how to run, portability limits (Windows/hardcoded paths/`winsound`), reproducibility.
   - Suggested best practices (not automatically implemented without validation).
   - Local validation status.

3. **`tests/test_path_safety.py` (new)**
   - Pure-Python tests (no external dependencies) validating that `os.path.join` does not escape the base directory and that `~$*.xlsx` locks are recognized.

## Not implemented (reason: avoid scientific regression without numerical validation/regression)
- `help_functions.py`: not changed.
- `model.py`: not changed.
- Extreme parameter validation (REA-003/004).
- Injected RNG (`default_rng`) (REA-002).
- CLI/importable entrypoint and `winsound`/profile guard (REA-001/006/007).
- `.gitignore` already covers `~$*` and `profile.txt` without changing source code.

## Validation
- `python -m py_compile model.py help_functions.py tests/test_path_safety.py` → OK.
- `python tests/test_path_safety.py` → OK.
- No simulation/benchmark execution (missing dependencies).
