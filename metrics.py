"""
metrics.py
Gera tabelas de Feature/LoC, interacoes a partir de outputs do PCLocator.
"""

import argparse
import os
from pathlib import Path
import sys

from src.processar_arquivos import processar_arquivos
from src.escrever_csv import escrever_csv_features, escrever_csv_interacoes, escrever_csv_agregado
from src.agregar_por_grau import agregar_por_grau



def main():
    parser = argparse.ArgumentParser(
        description="Gera tabelas de Feature/LoC, interacoes e metricas a partir de outputs do PCLocator."
    )
    parser.add_argument("pasta", help="Pasta raiz onde buscar os arquivos")
    parser.add_argument("--saida", default=None, help="Arquivo CSV de saida principal (default: <pasta>_LoC.csv)")
    parser.add_argument("--features", action="store_true", help="Gera apenas o CSV de features individuais")
    parser.add_argument("--interacoes", action="store_true", help="Gera apenas o CSV de interacoes")
    parser.add_argument("--agregado", action="store_true", help="Gera o CSV de agregado por grau de interacao (percentual de linhas em grau 1, 2, 3...)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Imprime cada ocorrencia encontrada")
    args = parser.parse_args()

    raiz = Path(args.pasta)
    if not raiz.is_dir():
        print(f"Pasta não encontrada: {raiz}", file=sys.stderr)
        sys.exit(1)

    output_folder = Path(f"./data/out/{raiz.name}_LoC.csv")

    saida = args.saida or output_folder

    gerar_tudo = not (args.features or args.interacoes)

    linhas_por_arquivo_feature, interacoes_por_arquivo, features_da_interacao, arquivos_processados = (
        processar_arquivos(raiz, verbose=args.verbose)
    )

    if arquivos_processados == 0:
        print("Nenhum arquivo com output do PCLocator foi encontrado", file=sys.stderr)
        sys.exit(1)


    base, ext = os.path.splitext(str(saida))
    ext = ext or ".csv"

    if gerar_tudo or args.features:
        escrever_csv_features(linhas_por_arquivo_feature, str(saida))
        print(f"CSV de features salvo em: {str(saida)}")

    if gerar_tudo or args.interacoes:
        caminho = f"{base}_interacoes{ext}"
        escrever_csv_interacoes(interacoes_por_arquivo, features_da_interacao, caminho)
        print(f"CSV de interacoes salvo em: {caminho}")

    if gerar_tudo or args.agregado:
        contagem_por_grau, total_linhas, percentual_por_grau = agregar_por_grau(
            linhas_por_arquivo_feature, interacoes_por_arquivo, features_da_interacao
        )
        caminho = f"{base}_agregado{ext}"
        escrever_csv_agregado(contagem_por_grau, total_linhas, percentual_por_grau, caminho)
        print(f"CSV de agregado salvo em: {caminho}")

    print(f"Arquivos processados: {arquivos_processados}")
    
if __name__ == "__main__":
    main()
