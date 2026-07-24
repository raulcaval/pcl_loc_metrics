def agregar_por_grau(linhas_por_arquivo_feature, interacoes_por_arquivo, features_da_interacao):

    # Mapeia (arquivo, numero_linha) -> grau para todas as linhas de interacao (grau >= 2)
    grau_da_linha = {}
    for (nome_arquivo, condicao), numeros in interacoes_por_arquivo.items():
        grau = len(features_da_interacao[(nome_arquivo, condicao)])
        for n in numeros:
            grau_da_linha[(nome_arquivo, n)] = grau  # uma condicao por linha, garantido pelo PCLocator

    todas_linhas = {
        (nome_arquivo, n)
        for (nome_arquivo, _feature), numeros in linhas_por_arquivo_feature.items()
        for n in numeros
    }
    
    # Linhas que nao estao em nenhuma interacao  = grau 1
    contagem_por_grau = {}
    for linha in todas_linhas:
        grau = grau_da_linha.get(linha, 1)
        contagem_por_grau[grau] = contagem_por_grau.get(grau, 0) + 1

    total_linhas = len(todas_linhas)
    percentual_por_grau = {
        grau: (count / total_linhas * 100)
        if total_linhas
            else 0.0
        for grau, count in contagem_por_grau.items()
    }

    return contagem_por_grau, total_linhas, percentual_por_grau