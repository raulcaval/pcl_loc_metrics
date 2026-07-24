import fnmatch
from pathlib import Path
import re


FEATURE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*") # regex para extrair features de uma condicao
HEADER_RE = re.compile(r"^\s*#\s*\|")              # linha "# | line of code | Merge |"
SEP_RE = re.compile(r"^[-+]+\s*$")                 # linha "-----+-----+-----+"
STATS_RE = re.compile(r"\+\d+MB.*ms")              # linha final "+MB, ms"
IGNORE_PATTERN = "*log.txt"


def extrair_features(condicao: str):
    # Retorna as features presentes numa condicao (string bruta da coluna Merge).
    if condicao.strip() in ("", "True"):
        return set()
    return set(FEATURE_RE.findall(condicao))


def parsear_colunas(linha_separador: str):
 
    posicoes = [i for i, ch in enumerate(linha_separador) if ch == "+"]
    colunas = []
    inicio = 0
    for pos in posicoes:
        colunas.append((inicio, pos))
        inicio = pos + 1
    return colunas


def extrair_linhas(texto: str):
    #Extrai (numero_da_linha, condicao) de cada linha de LoC da tabela do PCLocator.
    resultado = []
    dentro_da_tabela = False
    colunas = None

    for linha_raw in texto.splitlines():
        if HEADER_RE.match(linha_raw):
            dentro_da_tabela = True
            colunas = None
            continue

        if not dentro_da_tabela:
            continue

        if SEP_RE.match(linha_raw.strip()):
            if colunas is None:
                colunas = parsear_colunas(linha_raw)
            continue

        if "|" not in linha_raw:
            dentro_da_tabela = False
            continue

        if STATS_RE.search(linha_raw):
            continue

        if not colunas or len(colunas) < 3:
            continue

        index_str = linha_raw[colunas[0][0]:colunas[0][1]].strip()
        # print(f"DEBUG: index_str='{index_str}'")  # Debug
        condicao = linha_raw[colunas[2][0]:colunas[2][1]].strip()
        # print(f"DEBUG: condicao='{condicao}'")  # Debug

        if not index_str.isdigit():
            continue

        resultado.append((int(index_str), condicao))
    return resultado


def deve_ignorar(caminho: Path) -> bool:
    return fnmatch.fnmatch(caminho.name.lower(), IGNORE_PATTERN)


def encontrar_arquivos(raiz: Path):
    for caminho in sorted(raiz.rglob("*")):
        if caminho.is_file() and not deve_ignorar(caminho):
            yield caminho

def processar_arquivos(raiz: Path, verbose: bool = False):

    linhas_por_arquivo_feature = {}
    interacoes_por_arquivo = {}
    features_da_interacao = {}
    arquivos_processados = 0

    for arquivo in encontrar_arquivos(raiz):
        try:
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        except (UnicodeDecodeError, OSError):
            continue

        ocorrencias = extrair_linhas(texto)
        if not ocorrencias:
            continue

        arquivos_processados += 1
        nome_arquivo = arquivo.name

        for numero_linha, condicao in ocorrencias:
            features_da_linha = extrair_features(condicao)

            for feature in features_da_linha:
                linhas_por_arquivo_feature.setdefault((nome_arquivo, feature), []).append(numero_linha)
                if verbose:
                    print(f"Arquivo: {nome_arquivo}, Feature: {feature}, Linha: {numero_linha}")

            # Interacao = 2+ features na mesma condicao (coluna Merge).
            if len(features_da_linha) >= 2:
                key = (nome_arquivo, condicao)
                interacoes_por_arquivo.setdefault(key, []).append(numero_linha)
                features_da_interacao[key] = frozenset(features_da_linha)

    return linhas_por_arquivo_feature, interacoes_por_arquivo, features_da_interacao, arquivos_processados
