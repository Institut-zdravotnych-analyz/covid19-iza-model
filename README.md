# covid19-IZA-model

Covid19 pandemic wave agent-based model with intervention simulation (Covid Automat) for Slovakia.

## Escopo e segurança

Este repositório contém um modelo de pesquisa epidemiológica (agent-based) para ondas de COVID-19 na Eslováquia, com simulação de intervenções. É **código de pesquisa**, não um produto de saúde pública para tomada de decisão clínica. Resultados dependem de parâmetros, semente aleatória e dados de entrada; use com revisão técnica e validação independente antes de qualquer uso operacional.

## Dependências

O modelo roda em **Python** e depende de bibliotecas externas que não estão listadas no repositório:

- pandas
- numpy
- matplotlib
- scipy (interpolação)
- numexpr
- olefile / xlrd / pyxlsb (leitura de Excel legado, condicional)
- winsound (som — **apenas Windows**)

Não há `requirements.txt` nem lock file. Recomenda-se gerar um ambiente isolado (virtualenv/conda) e pinar versões para reprodução.

## Como executar

Os arquivos de entrada ficam em subpastas:

- `demografia/` — população por idade e distrito
- `params_data/` — parâmetros da doença, cronogramas de vacinação, R0, automat
- `testing_data/` — dados de testes
- `hospitalizacie_umrtia/` — internações e óbitos

O ponto de entrada é `model.py` (`if __name__ == '__main__'`). Ele possui caminhos hardcoded (ex.: `C:\Users\klukaa\Desktop\sim\`) e gera plots interativos (`plt.show`) e som (`winsound.Beep`), portanto **não é imediatamente portável para Linux/macOS** nem reproduzível sem ajustes de caminho e ambiente.

## Reprodutibilidade

- `np.random.seed(1)` é definido globalmente; o uso extensivo de `np.random.*` sem gerador injetado dificulta isolamento de corridas/testes.
- O script usa data corrente (`pd.to_datetime("today")`) em parte da análise final.
- Não há testes automatizados nem CI.

## Boas práticas sugeridas (não implementadas automaticamente sem nova validação)

1. Adicionar `requirements.txt` / lock file e smoke test determinístico com dataset sintético pequeno.
2. Extrair o núcleo da simulação para uma função importável via CLI (`argparse`), removendo efeitos colaterais do import.
3. Validar parâmetros extremos (`R0`, `test_ratio`, `protection_delay`, tamanhos de população, janelas temporais) com erros claros.
4. Isolar `winsound`, `plt.show()` e caminhos atrás de flags/ambiente.
5. Substituir RNG global por `numpy.random.Generator` passado como dependência.

## Validação local desta auditoria

- `python -m py_compile model.py help_functions.py` → sintaxe OK.
- Não foi possível executar simulações/benchmarks (dependências `numpy/pandas/scipy/numexpr/matplotlib` ausentes no ambiente; **Julia não instalada**).
