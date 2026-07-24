import csv


def escrever_csv_features(linhas_por_arquivo_feature, caminho):
    # Grava o CSV principal:(arquivo, feature, LoC, Linhas).
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Arquivo", "Feature", "LoC", "Linhas"])

        itens = sorted(linhas_por_arquivo_feature.items(), key=lambda x: (x[0][0], -len(x[1])))
        for (nome_arquivo, feature), numeros in itens:
            numeros = sorted(numeros)
            writer.writerow([nome_arquivo, feature, len(numeros), ",".join(map(str, numeros))])


def escrever_csv_interacoes(interacoes_por_arquivo, features_da_interacao, caminho):
    # Grava o CSV de interacoes: (arquivo, condicao, grau, LoC, Linhas).
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Arquivo", "Features", "Grau", "LoC", "Linhas"])

        itens = sorted(
            interacoes_por_arquivo.items(),
            key=lambda x: (x[0][0], -len(features_da_interacao[x[0]]), -len(x[1])),  # arquivo, grau, ocorrencias
        )
        for (nome_arquivo, condicao), numeros in itens:
            numeros = sorted(numeros)
            grau = len(features_da_interacao[(nome_arquivo, condicao)])
            writer.writerow([nome_arquivo, condicao, grau, len(numeros), ",".join(map(str, numeros))])


def escrever_csv_agregado(contagem_por_grau, total_linhas, percentual_por_grau, caminho):
    # Grava o CSV agregado: (grau, LoC, percentual).
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Grau", "LoC", "Percentual %"])
        writer.writerow(["TOTAL", total_linhas, "100.00"])

        for grau in sorted(contagem_por_grau.keys()):
            writer.writerow([
                grau,
                contagem_por_grau[grau],
                f"{percentual_por_grau[grau]:.2f}",
            ])