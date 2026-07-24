"""
Executa o PCLocator em arquivos .c recursivamente
e salva os resultados em arquivos .txt, mantendo a estrutura de pastas.

uso:
    uv run pcl.py <caminho_para_PCLocator.jar> <pasta_raiz_arquivos_c> [ (optional) --saida <arquivo_saida>]
""" 

import argparse
from pathlib import Path
import subprocess
import sys

TIMEOUT_SECONDS = 30


def main():
    parser = argparse.ArgumentParser(
        description=" Roda a ferramenta PCLocator em todos os arquivos"
        " .c de uma pasta recursivamente e salva os resultados em um txt" \
        " respeitando a estrutura de pastas."
    )
    parser.add_argument("pclocator",  help="caminho para o arquivo PCLocator.jar")
    parser.add_argument("pasta",  help="Pasta raiz onde buscar os arquivos")
    args = parser.parse_args()

    processed = 0
    skipped = 0

    prog_java = Path(args.pclocator)
    folder_path = Path(args.pasta)
    output_folder = Path(f"./data/processed/_{folder_path.name}")

    output_folder.mkdir(exist_ok=True)
    err_log = output_folder / "err_log.txt"

    if not folder_path.is_dir():
        print(f"Pasta não encontrada: {folder_path}", file=sys.stderr)
        sys.exit(1)
        
    for file_path in folder_path.rglob("*.c"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(folder_path)
        output_subfolder = output_folder / relative_path.parent
        output_subfolder.mkdir(parents=True, exist_ok=True)

        try:
            resultado = subprocess.run(
                ["java", "-jar", prog_java, "--annotator", "merge", file_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=TIMEOUT_SECONDS
            )

            output_file = output_subfolder / f"{file_path.stem}.txt"
            with open(output_file, "w", encoding="utf-8") as out_file:
                out_file.write(f"FILE: {file_path}\n")
                out_file.write("Resultado PCLocator:\n")
                out_file.write(resultado.stdout)

            print(f"Processado: {file_path} -> Resultado salvo em: {output_file}")
            processed += 1

        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {file_path} — pulando.")
            skipped += 1

            with open(err_log, "a", encoding="utf-8") as log:
                log.write(f"FILE: {file_path}\n")
                log.write(f"ERRO: TIMEOUT após {TIMEOUT_SECONDS}s\n")
                log.write("-" * 60 + "\n")

        except subprocess.CalledProcessError as e:
            print(f"[ERRO] {file_path} — pulando.")
            skipped += 1

            with open(err_log, "a", encoding="utf-8") as log:
                log.write(f"FILE: {file_path}\n")
                log.write(f"OCORREU UM ERRO AO EXECUTAR O PROGRAMA {prog_java}:\n")
                log.write(e.stderr)
                log.write("-" * 60 + "\n")

    print(f"\nExecução concluída! Resultados salvos em: {output_folder}")
    print(f"  Processados: {processed} | Pulados/Erros: {skipped}")
    if skipped:
        print(f"  Log de erros: {err_log}")

if __name__ == "__main__":
    main()