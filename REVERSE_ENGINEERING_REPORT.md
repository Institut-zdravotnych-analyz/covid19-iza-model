# Reverse Engineering / Auditoria — covid19-iza-model

## Escopo
- **Repositório:** https://github.com/Institut-zdravotnych-analyz/covid19-iza-model
- **Base:** `9e62ba6` (branch `main`), clone local `C:\Users\User\audit-repos\covid19-iza-model`.
- **Modo:** Fase 1 estática (inspeção/leitura, sem executar simulações); Fase 2 corrigir/documentar e publicar, com autorização expressa do usuário.
- **Limitações:** sem `numpy/pandas/scipy/numexpr/matplotlib/openpyxl/xlrd/pyxlsb` no ambiente; **Julia não instalada**. Não houve execução de simulações/benchmarks/reprodução numérica. `python -m py_compile` passou em `model.py`, `help_functions.py` e `tests/test_path_safety.py`.

## Fase 1 — Diagnóstico geral
- **Arquitetura:** modelo agent-based epidemiológico (COVID-19, Eslováquia) com componentes: inicialização demográfica/etária/distrital, vacinação, resistência/imunidade, infecção diária, “automat” (níveis/restrições), logging e plots.
- **Tecnologias:** Python, `numpy`, `pandas`, `matplotlib`, `scipy.interpolate`, `numexpr`, `cProfile`, `winsound` (Windows), `olefile`/Excel engines.
- **Manutenção:** snapshot de pesquisa/operacional (datas/comentários de 2021, caminhos hardcoded, blocos comentados). README mínimo. Sem `requirements.txt`, CI ou testes.
- **Público:** 0 Issues e 0 PRs listados no GitHub (estado atual).

## Problemas investigados (IDs REA)
| ID | Sev | Status | Local | Resumo |
|---|---|---|---|---|
| REA-001 | P1 | CONFIRMADO | `model.py` `__main__`/`full_sim` | Execução não reproduzível/segura: caminhos hardcoded (`C:\Users\klukaa\...`), `winsound` (Windows-only), `break` após 1 cenário, `exit()` em ramos, `plt.show`, `pd.to_datetime("today")`. |
| REA-002 | P1 | CONFIRMADO | `model.py:424` | `np.random.seed(1)` global e RNG não injetado; estado global vaza entre corridas/testes. |
| REA-003 | P1 | PROVÁVEL | `model.py:112, 222, 223, 266+` | Divisões por `protection_delay`, `test_ratio`, `len(df)`, `spolu` sem guarda contra zero → `inf/NaN` ou `ZeroDivisionError` com parâmetros extremos. |
| REA-004 | P2 | CONFIRMADO | `model.py:179-180` | `np.random.geometric(1/(R0/infectious_l[j]+1), n)` pode ser inválido com `R0` extremo/negativo. |
| REA-005 | P2 | CONFIRMADO | `help_functions.py:21-36` | `save_df` sobrescreve silenciosamente (`os.remove`); extensões desconhecidas só imprimem. |
| REA-006 | P2 | CONFIRMADO | `model.py:26-27` | Decorator `profile` escreve `profile.txt` no cwd (efeito colateral). |
| REA-007 | P2 | CONFIRMADO | `model.py:10,1047`; `help_functions.py` | `winsound` quebra em Linux/macOS; leitura Excel depende de engines opcionais sem verificação clara. |
| REA-008 | P2 | CONFIRMADO | `help_functions.py:415` | Lógica de path assume separador Windows `\\` em alguns trechos; portabilidade frágil. |
| REA-009 | P2 | PROVÁVEL | `model.py` automat/`novy_automat` | `DataFrame.append` (depreciado) em laços e janelas temporais fixas; dados curtos podem gerar slices vazios/NaN. |
| REA-010 | P2 | CONFIRMADO | `params_data/~$*.xlsx` | Arquivos temporários do Excel rastreados no repo; risco de confusão. |
| REA-011 | P3 | CONFIRMADO | Repositório | Sem deps declaradas, lock, testes, CI, README insuficiente. |
| REA-012 | P3 | CONFIRMADO | `model.py`/`help_functions.py` | Blocos comentados, prints, `if False`, constantes mágicas, `exit()`/checks “lazy function is broken”. |

## Problemas recorrentes
Nenhum documentado publicamente (0 Issues/PRs). Não inventado.

## Mudanças implementadas (Fase 2)
1. `.gitignore` (novo): ignora `__pycache__/`, `*.py[cod]`, `.venv/`, `profile.txt`, `*.log`, `~$*.xlsx`, `~$*.xls`, `*.ipynb_checkpoints/`, `.DS_Store`, `Thumbs.db`. **Não ignora dados de entrada rastreados** (CSV/XLSX do repo).
2. `README.md` expandido: escopo/segurança, dependências, como executar, limites de portabilidade (Windows/caminhos hardcoded), reprodutibilidade e boas práticas sugeridas.
3. `tests/test_path_safety.py` (novo): testes puros em Python (sem deps) validando que `os.path.join` não escapa do diretório base e que locks `~$*.xlsx` são reconhecidos.
4. `help_functions.py`: **não alterado** (restaurado ao HEAD) para evitar regressão científica sem validação numérica.
5. `model.py`: **não alterado** (restaurado ao HEAD) para evitar regressão científica sem validação numérica.

## Mudanças NÃO implementadas (precisam de validação numérica/regressão)
- Validação de parâmetros extremos (REA-003/004): exige testes com seed fixa e dataset controlado antes/depois.
- RNG injetado / `default_rng` (REA-002): pode alterar resultados estocásticos se mudar ordem do RNG.
- Entrada CLI/importável, guarda `winsound`/profile (REA-001/006/007): seguro, mas fora do escopo mínimo aprovado nesta rodada.

## Validação executada
- `python -m py_compile model.py help_functions.py tests/test_path_safety.py` → OK.
- `python tests/test_path_safety.py` → OK.
- Não executado: simulação completa, benchmarks, regressão numérica (deps/dados de runtime indisponíveis).

## Riscos remanescentes
- Resultados científicos dependem de semente e ordem do RNG; mudanças no RNG exigem regressão.
- Caminhos hardcoded e `winsound` limitam execução fora do ambiente original do autor.
- Sem testes de regressão com dados reais.
