# Correções — covid19-iza-model

Base: `Institut-zdravotnych-analyz/covid19-iza-model@9e62ba6` (main). Usuário autorizou implementação de todas as propostas viáveis.

## Implementado

1. **`.gitignore` (novo)**
   - Ignora caches Python, `profile.txt`, `*.log`, locks temporários do Excel (`~$*.xlsx`/`~$*.xls`), checkpoints de notebook, `.DS_Store`, `Thumbs.db`.
   - **Não ignora** arquivos de entrada rastreados (CSV/XLSX do repo).

2. **`README.md` (atualizado)**
   - Escopo e segurança (pesquisa, não produto clínico; revisão técnica obrigatória).
   - Dependências, como executar, limites de portabilidade (Windows/caminhos hardcoded/`winsound`), reprodutibilidade.
   - Boas práticas sugeridas (não implementadas automaticamente sem validação).
   - Status de validação local.

3. **`tests/test_path_safety.py` (novo)**
   - Testes puros em Python (sem dependências externas) validando que `os.path.join` não escapa do diretório base e que locks `~$*.xlsx` são reconhecidos.

## Não implementado (motivo: evitar regressão científica sem validação numérica/regressão)
- `help_functions.py`: não alterado.
- `model.py`: não alterado.
- Validação de parâmetros extremos (REA-003/004).
- RNG injetado (`default_rng`) (REA-002).
- Entrada CLI/importável e guarda `winsound`/profile (REA-001/006/007).
- `.gitignore` já cobre `~$*` e `profile.txt` sem alterar código-fonte.

## Validação
- `python -m py_compile model.py help_functions.py tests/test_path_safety.py` → OK.
- `python tests/test_path_safety.py` → OK.
- Sem execução de simulação/benchmark (dependências ausentes).
