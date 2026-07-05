#!/usr/bin/env python3
"""
Automação dos Experimentos de Algoritmos de Ordenação
=====================================================
Trabalho Prático: Benchmarking e Análise Empírica de Algoritmos de Ordenação

Este script:
  1. Compila todos os algoritmos em C (usando GCC)
  2. Executa os 3 problemas do trabalho
  3. Salva os resultados em CSV na pasta data/
  4. Gera gráfico de barras para o Problema 2
"""

import os
import sys
import subprocess
import shutil
import csv
import resource


# ============================================================
# Configurações de cores para o terminal
# ============================================================
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    NEGRITO = '\033[1m'
    FIM = '\033[0m'


def log_info(msg):
    print(f"{Cores.AZUL}[INFO]{Cores.FIM} {msg}")

def log_sucesso(msg):
    print(f"{Cores.VERDE}[SUCESSO]{Cores.FIM} {Cores.NEGRITO}{msg}{Cores.FIM}")

def log_aviso(msg):
    print(f"{Cores.AMARELO}[AVISO]{Cores.FIM} {msg}")

def log_erro(msg):
    print(f"{Cores.VERMELHO}[ERRO]{Cores.FIM} {msg}")


# ============================================================
# Aumentar o limite de stack (equivalente a ulimit -s unlimited)
# Necessário para o Quicksort no Problema 2 (vetor ordenado)
# ============================================================
def aumentar_stack():
    """Aumenta o limite de stack para evitar Stack Overflow no Quicksort."""
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
        # Define o soft limit como o hard limit (máximo permitido)
        resource.setrlimit(resource.RLIMIT_STACK, (hard, hard))
        log_info(f"Limite de stack aumentado: {soft} -> {hard} bytes")
    except (ValueError, resource.error) as e:
        log_aviso(f"Não foi possível aumentar o limite de stack: {e}")
        log_aviso("Considere rodar 'ulimit -s unlimited' antes de executar este script.")


# ============================================================
# Compilação
# ============================================================
def encontrar_gcc():
    """Busca o compilador GCC no PATH."""
    gcc_path = shutil.which("gcc")
    if gcc_path:
        return gcc_path
    return None


def compilar_projeto(gcc_path):
    """Compila todos os 6 algoritmos de ordenação."""
    log_info(f"Usando compilador: {gcc_path}")
    os.makedirs("bin", exist_ok=True)

    algoritmos = ["bubblesort", "heapsort", "insertionsort",
                  "quicksort", "selectionsort", "shellsort"]
    cflags = ["-Wall", "-Wextra", "-O3", "-std=gnu99"]

    for alg in algoritmos:
        saida = os.path.join("bin", alg)
        src_alg_c = os.path.join("src", alg, f"{alg}.c")
        src_main_c = os.path.join("src", alg, "main.c")
        src_ordenacao_c = os.path.join("src", "ordenacao.c")

        cmd = [gcc_path] + cflags + [src_main_c, src_alg_c, src_ordenacao_c, "-o", saida, "-lm"]

        log_info(f"Compilando {alg}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            log_erro(f"Falha ao compilar {alg}:")
            print(res.stderr)
            sys.exit(1)

    log_sucesso("Todos os algoritmos foram compilados com sucesso!")


# ============================================================
# Execução de binários
# ============================================================
def executar_binario(alg, args):
    """Executa um binário compilado e retorna o stdout."""
    caminho_bin = os.path.join("bin", alg)
    cmd = [caminho_bin] + [str(a) for a in args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        log_erro(f"Erro ao executar {alg}: {res.stderr}")
        sys.exit(1)
    return res.stdout.strip()


# ============================================================
# Geração de gráfico (Problema 2)
# ============================================================
def gerar_grafico(heapsort_dados, quicksort_dados):
    """Gera gráfico de barras comparando Heapsort vs Quicksort (Problema 2)."""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend não-interativo
        import matplotlib.pyplot as plt
    except ImportError:
        log_aviso("Matplotlib não encontrado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except (subprocess.CalledProcessError, ImportError):
            log_aviso("Não foi possível instalar matplotlib automaticamente.")
            log_aviso("Para gerar o gráfico, ative o venv e instale manualmente:")
            log_aviso("  source venv/bin/activate && pip install matplotlib")
            return

    log_info("Gerando gráfico de barras para o Problema 2...")

    algoritmos = ['Heapsort', 'Quicksort']
    tempos_medios = [float(heapsort_dados['tempo']), float(quicksort_dados['tempo'])]
    desvios = [float(heapsort_dados['desvio']), float(quicksort_dados['desvio'])]

    fig, ax = plt.subplots(figsize=(8, 6))
    cores_barras = ['#3498db', '#e74c3c']

    barras = ax.bar(
        algoritmos, tempos_medios, yerr=desvios, align='center',
        alpha=0.85, ecolor='black', capsize=10, color=cores_barras, width=0.5
    )

    ax.set_ylabel('Tempo Médio de Execução (segundos)', fontsize=12, fontweight='bold')
    ax.set_title(
        'Problema 2: Heapsort vs Quicksort (Vetor Ordenado, N=5000)\n'
        'Tempo Médio com Desvio Padrão (10 execuções)',
        fontsize=13, fontweight='bold', pad=20
    )
    ax.yaxis.grid(True, linestyle='--', alpha=0.6)

    for bar in barras:
        height = bar.get_height()
        ax.annotate(
            f'{height:.6f} s',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    plt.tight_layout()
    os.makedirs("data", exist_ok=True)
    plt.savefig(os.path.join("data", "grafico_problema_2.png"), dpi=300)
    plt.close()
    log_sucesso("Gráfico salvo em 'data/grafico_problema_2.png'")


# ============================================================
# Programa Principal
# ============================================================
def main():
    print(f"\n{Cores.NEGRITO}{'=' * 66}{Cores.FIM}")
    print(f"{Cores.NEGRITO}   Automação dos Experimentos de Algoritmos de Ordenação{Cores.FIM}")
    print(f"{Cores.NEGRITO}{'=' * 66}{Cores.FIM}\n")

    # ---------------------------------------------------------
    # 0. Aumentar limite de stack (para o Quicksort)
    # ---------------------------------------------------------
    aumentar_stack()

    # ---------------------------------------------------------
    # 1. Encontrar GCC e compilar
    # ---------------------------------------------------------
    gcc_path = encontrar_gcc()
    if not gcc_path:
        log_erro("Compilador GCC não encontrado! Instale o GCC e tente novamente.")
        sys.exit(1)

    log_info(f"GCC encontrado em: {gcc_path}")
    compilar_projeto(gcc_path)

    # Prepara pasta de dados
    os.makedirs("data", exist_ok=True)

    # =========================================================
    # PROBLEMA 1: Custo de Operações Teóricas vs. Tempo Real
    # =========================================================
    print(f"\n{Cores.NEGRITO}--- Problema 1 (N = 30.000) ---{Cores.FIM}")
    prob1_algs = ["bubblesort", "insertionsort", "selectionsort"]
    cenarios = {1: "Aleatorio", 2: "Ordenado", 3: "Inverso"}

    tabela_prob1 = []
    for alg in prob1_algs:
        for c_id, cen_nome in cenarios.items():
            log_info(f"  -> Rodando {alg} no cenário {cen_nome}...")
            output = executar_binario(alg, [30000, c_id])
            parts = output.split(",")
            # Formato: Algoritmo,Cenario,Tempo,Comparacoes,Trocas
            nome_alg = parts[0]
            cen = parts[1]
            tempo = float(parts[2])
            comp = int(parts[3])
            trocas = int(parts[4])
            tabela_prob1.append({
                'algoritmo': nome_alg,
                'cenario': cen,
                'tempo': tempo,
                'comparacoes': comp,
                'trocas': trocas
            })

    # Salva CSV do Problema 1
    prob1_csv = os.path.join("data", "tabela_problema_1.csv")
    with open(prob1_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo (s)", "Comparacoes", "Trocas"])
        for row in tabela_prob1:
            writer.writerow([row['algoritmo'], row['cenario'],
                             f"{row['tempo']:.6f}", row['comparacoes'], row['trocas']])
    log_sucesso(f"Resultados do Problema 1 salvos em '{prob1_csv}'")

    # =========================================================
    # PROBLEMA 2: O Desafio do Quicksort Clássico
    # =========================================================
    print(f"\n{Cores.NEGRITO}--- Problema 2 (N = 5.000, 10 execuções, Vetor Ordenado) ---{Cores.FIM}")
    prob2_dados = {}
    for alg in ["heapsort", "quicksort"]:
        log_info(f"  -> Rodando {alg} (10 execuções)...")
        output = executar_binario(alg, [5000])
        parts = output.split(",")
        # Formato: Algoritmo,Cenario,TempoMedio,DesvioPadrao,Comparacoes,Trocas
        prob2_dados[alg] = {
            'nome': parts[0],
            'cenario': parts[1],
            'tempo': parts[2],
            'desvio': parts[3],
            'comparacoes': parts[4],
            'trocas': parts[5]
        }

    # Salva CSV do Problema 2
    prob2_csv = os.path.join("data", "tabela_problema_2.csv")
    with open(prob2_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo Medio (s)",
                         "Desvio Padrao (s)", "Comparacoes", "Trocas"])
        for alg in ["heapsort", "quicksort"]:
            d = prob2_dados[alg]
            writer.writerow([d['nome'], "Ordenado", d['tempo'],
                             d['desvio'], d['comparacoes'], d['trocas']])
    log_sucesso(f"Resultados do Problema 2 salvos em '{prob2_csv}'")

    # Gráfico de barras
    gerar_grafico(prob2_dados['heapsort'], prob2_dados['quicksort'])

    # =========================================================
    # PROBLEMA 3: Dados Quase-Ordenados e o Shellsort
    # =========================================================
    print(f"\n{Cores.NEGRITO}--- Problema 3 (N = 50.000, Vetor Quase Ordenado) ---{Cores.FIM}")
    tabela_prob3 = []
    for alg in ["insertionsort", "shellsort"]:
        log_info(f"  -> Rodando {alg}...")
        if alg == "insertionsort":
            output = executar_binario(alg, [50000, 4])
        else:
            output = executar_binario(alg, [50000])
        parts = output.split(",")
        nome_alg = parts[0]
        cen = parts[1]
        tempo = float(parts[2])
        comp = int(parts[3])
        trocas = int(parts[4])
        tabela_prob3.append({
            'algoritmo': nome_alg,
            'cenario': cen,
            'tempo': tempo,
            'comparacoes': comp,
            'trocas': trocas
        })

    # Salva CSV do Problema 3
    prob3_csv = os.path.join("data", "tabela_problema_3.csv")
    with open(prob3_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo (s)", "Comparacoes", "Trocas"])
        for row in tabela_prob3:
            writer.writerow([row['algoritmo'], row['cenario'],
                             f"{row['tempo']:.6f}", row['comparacoes'], row['trocas']])
    log_sucesso(f"Resultados do Problema 3 salvos em '{prob3_csv}'")

    # =========================================================
    # Resultados Gerais consolidados
    # =========================================================
    gerais_csv = os.path.join("data", "resultados_gerais.csv")
    with open(gerais_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Problema", "Algoritmo", "Cenario", "Tempo (s)",
                         "Desvio Padrao (s)", "Comparacoes", "Trocas"])
        for row in tabela_prob1:
            writer.writerow(["1", row['algoritmo'], row['cenario'],
                             f"{row['tempo']:.6f}", "", row['comparacoes'], row['trocas']])
        for alg in ["heapsort", "quicksort"]:
            d = prob2_dados[alg]
            writer.writerow(["2", d['nome'], "Ordenado",
                             d['tempo'], d['desvio'], d['comparacoes'], d['trocas']])
        for row in tabela_prob3:
            writer.writerow(["3", row['algoritmo'], row['cenario'],
                             f"{row['tempo']:.6f}", "", row['comparacoes'], row['trocas']])
    log_sucesso(f"Resultados consolidados salvos em '{gerais_csv}'")

    # =========================================================
    # RESUMO NO CONSOLE
    # =========================================================
    print(f"\n{Cores.NEGRITO}{'=' * 76}{Cores.FIM}")
    print(f"{Cores.NEGRITO}{'RESUMO DOS RESULTADOS':^76}{Cores.FIM}")
    print(f"{Cores.NEGRITO}{'=' * 76}{Cores.FIM}")

    # Problema 1
    print(f"\n{Cores.NEGRITO}Problema 1: Custo Teórico vs. Tempo Real (N = 30.000){Cores.FIM}")
    print(f"{'Algoritmo':<16} | {'Cenário':<12} | {'Tempo (s)':<12} | {'Comparações':<14} | {'Trocas':<14}")
    print("-" * 76)
    for row in tabela_prob1:
        print(f"{row['algoritmo']:<16} | {row['cenario']:<12} | "
              f"{row['tempo']:<12.6f} | {row['comparacoes']:<14} | {row['trocas']:<14}")

    # Problema 2
    print(f"\n{Cores.NEGRITO}Problema 2: Heapsort vs. Quicksort (N = 5.000, 10 execuções, Ordenado){Cores.FIM}")
    print(f"{'Algoritmo':<16} | {'Tempo Médio (s)':<16} | {'Desvio Padrão':<14} | {'Comparações':<14} | {'Trocas':<14}")
    print("-" * 82)
    for alg in ["heapsort", "quicksort"]:
        d = prob2_dados[alg]
        print(f"{d['nome']:<16} | {float(d['tempo']):<16.6f} | "
              f"{float(d['desvio']):<14.6f} | {int(d['comparacoes']):<14} | {int(d['trocas']):<14}")

    # Problema 3
    print(f"\n{Cores.NEGRITO}Problema 3: Insertionsort vs. Shellsort (N = 50.000, Quase Ordenado){Cores.FIM}")
    print(f"{'Algoritmo':<16} | {'Cenário':<16} | {'Tempo (s)':<12} | {'Comparações':<14} | {'Trocas':<14}")
    print("-" * 80)
    for row in tabela_prob3:
        print(f"{row['algoritmo']:<16} | {row['cenario']:<16} | "
              f"{row['tempo']:<12.6f} | {row['comparacoes']:<14} | {row['trocas']:<14}")

    print(f"\n{Cores.NEGRITO}{'=' * 76}{Cores.FIM}")
    log_sucesso("Processo finalizado! Dados e gráficos na pasta 'data/'.")
    print(f"{Cores.NEGRITO}{'=' * 76}{Cores.FIM}\n")


if __name__ == "__main__":
    main()
