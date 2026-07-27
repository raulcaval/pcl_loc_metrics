# spl-loc-analyzer

Projeto da disciplina Tópicos Avançados em Linguagens de Programação 2 — Software Product Lines (CInUFPE).

Ferramenta de linha de comando para análise estática de **Software Product Lines (SPL)** em projetos C.
A partir dos arquivos de saída do [PCLocator](https://github.com/ekuiter/PCLocator), extrai métricas de Loc de features condicionais (`#ifdef`/`#if defined`), gerando relatórios em CSV.

---

## Saídas geradas

| Arquivo | Conteúdo |
|---|---|
| `<saida>.csv` | LoC por `(arquivo, feature)` |
| `<saida>_interacoes.csv` | Interações N-way entre features (condições compostas) |
| `<saida>_agregado.csv` | Distribuição percentual de linhas por grau de interação |

---

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — gerenciador de pacotes e ambientes Python

```bash
# Instalar uv (caso não tenha)
curl -Ls https://astral.sh/uv/install.sh | sh
```

O projeto não possui dependências externas além da biblioteca padrão do Python — `uv` é usado apenas para gerenciar o ambiente isolado.

### Installing

```bash
# 1. Clonar o repositório
git clone https://github.com/raulcaval/spl-loc-analyzer.git
cd spl-loc-analyzer
```

---

## Usage

```bash
# Executa o PCLocator em arquivos .c recursivamente e salva os resultados em arquivos .txt, mantendo a estrutura de pastas.( saída padrão: /data/processed/<arquivos_processados> )
uv run pcl.py <caminho_para_PCLocator.jar> <pasta_raiz_arquivos_c>
```
---

```bash

# Gerar todos os CSVs (saída padrão: /data/out/ <pasta>_LoC.csv)
uv run metrics.py <pasta_outputs_pclocator>

# Especificar nome do arquivo de saída
uv run metrics.py <pasta_outputs_pclocator> --saida resultado.csv

# Gerar apenas o CSV de features individuais
uv run metrics.py <pasta> --saida features.csv --features

# Gerar apenas as interações entre features
uv run metrics.py <pasta> --saida interacoes.csv --interacoes

# Gerar apenas o agregado por grau de interação / porcentagem
uv run metrics.py <pasta> --saida agregado.csv --agregado

# Modo verbose: imprime cada ocorrência encontrada
uv run metrics.py <pasta> --saida resultado.csv -v
```

### Exemplo de saída — `resultado_agregado.csv`

```
Grau,LoC,Percentual %
TOTAL,76664,100.00
1,52662,68.69
2,15014,19.58
3,4862,6.34
4,1937,2.53
5,1400,1.83
6,212,0.28
7,202,0.26
8,18,0.02
9,14,0.02
10,19,0.02
11,1,0.00
12,2,0.00
15,315,0.41
17,1,0.00
19,5,0.01
```

---

## Metrics


### Grau de interação (N-way)

Cada linha de código recebe um grau igual ao número de features simultâneas na sua condição Merge:

- **Grau 1** — linha isolada (`#ifdef A`)
- **Grau 2** — interação 2-way (`#if defined(A) && defined(B)`)
- **Grau N** — interação N-way
---

## Project Structure

```
spl-loc-analyzer/
├─ .python-version
├─ _README.md
├─ data
│  ├─ base
│  ├─ out
│  │  ├─ _busybox-1.38.0_LoC.csv
│  │  ├─ _busybox-1.38.0_LoC_agregado.csv
│  │  └─ _busybox-1.38.0_LoC_interacoes.csv
│  ├─ processed
│  └─ raw
├─ docs
│  └─ Apresentacao_metricas_pclocator.pdf
├─ metrics.py
├─ pcl.py
├─ pyproject.toml
├─ src
│  ├─ agregar_por_grau.py
│  ├─ escrever_csv.py
│  └─ processar_arquivos.py
├─ tests
└─ uv.lock

```

---

## Built With

- [Python](https://www.python.org/) 3.10+
- [uv](https://docs.astral.sh/uv/) — gerenciamento de ambiente
- [PCLocator](https://github.com/ekuiter/PCLocator) — ferramenta externa que gera os arquivos de entrada

---

## Authors

- **Raul Cavalcanti** — [@raulcaval](https://github.com/raulcaval)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

