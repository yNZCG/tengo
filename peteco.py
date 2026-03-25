"""
Processador de Log - Serial + Paralelo com Pool
Executa com 2, 4, 8 e 12 processos e mede os tempos.
"""

import os
import glob
import time
import multiprocessing

PASTA = "log2"


def processar_arquivo(caminho):
    linhas = palavras = caracteres = 0
    contagem = {"erro": 0, "warning": 0, "info": 0}

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linhas += 1
            caracteres += len(linha)
            partes = linha.split()
            palavras += len(partes)
            for p in partes:
                if p in contagem:
                    contagem[p] += 1

    return linhas, palavras, caracteres, contagem


def consolidar(resultados):
    total_l = total_p = total_c = 0
    total_k = {"erro": 0, "warning": 0, "info": 0}
    for l, p, c, k in resultados:
        total_l += l
        total_p += p
        total_c += c
        for chave in total_k:
            total_k[chave] += k[chave]
    return total_l, total_p, total_c, total_k


def exibir(num_arquivos, tempo, total_l, total_p, total_c, total_k, modo):
    print(f"=== EXECUÇÃO {modo} ===")
    print(f"Arquivos processados: {num_arquivos}")
    print(f"Tempo total: {tempo:.4f} segundos")
    print(f"\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {total_l}")
    print(f"Total de palavras: {total_p}")
    print(f"Total de caracteres: {total_c}")
    print(f"\nContagem de palavras-chave:")
    for chave, valor in total_k.items():
        print(f"  {chave}: {valor}")


if __name__ == "__main__":
    arquivos = sorted(glob.glob(os.path.join(PASTA, "*.txt")))

    # ── Serial ──────────────────────────────────────────────
    inicio = time.time()
    resultados = [processar_arquivo(a) for a in arquivos]
    tempo_serial = time.time() - inicio
    tl, tp, tc, tk = consolidar(resultados)
    exibir(len(arquivos), tempo_serial, tl, tp, tc, tk, "SERIAL")

    # ── Paralelo ────────────────────────────────────────────
    for n in [2, 4, 8, 12]:
        print(f"\n{'='*40}")
        inicio = time.time()
        with multiprocessing.Pool(processes=n) as pool:
            resultados = pool.map(processar_arquivo, arquivos)
        tempo_paralelo = time.time() - inicio
        tl, tp, tc, tk = consolidar(resultados)
        speedup = tempo_serial / tempo_paralelo
        exibir(len(arquivos), tempo_paralelo, tl, tp, tc, tk, f"PARALELA ({n} processos)")
        print(f"Speedup: {speedup:.4f}x")