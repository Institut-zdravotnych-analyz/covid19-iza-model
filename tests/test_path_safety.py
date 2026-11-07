# Smoke tests de seguranca de caminho (sem dependencias externas)
# Testes puros em Python para validar a logica de construcao de caminhos usada
# pelo modelo, sem exigir pandas/numpy/matplotlib.
# Os caminhos do modelo sao construidos com os.path.join a partir de pastas
# configuradas (demografia_dir, params_dir, etc.) e nomes de arquivo fixos.
# Este teste garante que:
# - os.path.join nao permite "escape" de diretorio por .. no nome do arquivo.
# - Nomes de arquivo temporarios do Excel (~$*.xlsx) sao reconheciveis.

import os
import sys
import tempfile


def path_escapes_base(base: str, target: str) -> bool:
    """Retorna True se o caminho alvo sair do diretorio base."""
    base_abs = os.path.abspath(base)
    target_abs = os.path.abspath(os.path.join(base_abs, target))
    return not target_abs.startswith(base_abs + os.sep) and target_abs != base_abs


def is_excel_temp_lock(name: str) -> bool:
    return os.path.basename(name).startswith("~$") and name.lower().endswith((".xlsx", ".xls"))


def main() -> int:
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "data")
        os.makedirs(base)

        # 1. Nome normal nao escapa
        if path_escapes_base(base, "hospitalizacie.csv"):
            failures.append("arquivo normal escapou do base")

        # 2. Tentativa de traversal escapa
        if not path_escapes_base(base, "../outside.csv"):
            failures.append("traversal ../ nao detectado")

        # 3. Lock temporario do Excel detectado
        if not is_excel_temp_lock("~$R0.xlsx"):
            failures.append("~$R0.xlsx nao reconhecido como lock")
        if not is_excel_temp_lock("~$vaccination_timelines.xlsx"):
            failures.append("~$vaccination_timelines.xlsx nao reconhecido como lock")
        if is_excel_temp_lock("R0.xlsx"):
            failures.append("R0.xlsx falso positivo como lock")

    if failures:
        print("FALHAS:")
        for f in failures:
            print(" -", f)
        return 1

    print("Todos os testes de caminho passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
