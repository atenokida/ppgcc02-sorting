import os
import sys
import subprocess
import shutil
import csv
import time
import math

# Aumenta o limite de recursão para permitir o Quicksort em vetores ordenados no Python fallback
sys.setrecursionlimit(30000)

# Configurações de cores para o terminal
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

# Gerador de números pseudo-aleatórios compatível com MSVCRT rand()
class CRand:
    def __init__(self, seed=42):
        self.state = seed
    def rand(self):
        self.state = (self.state * 214013 + 2531011) & 0xFFFFFFFF
        return (self.state >> 16) & 0x7FFF

def gerar_vetor_aleatorio(n):
    crand = CRand(42)
    v = [0] * n
    for i in range(n):
        r1 = crand.rand()
        r2 = crand.rand()
        v[i] = ((r1 << 15) | r2) % 100000
    return v

def gerar_vetor_ordenado(n):
    return list(range(n))

def gerar_vetor_inverso(n):
    return [n - i for i in range(n)]

def gerar_vetor_quase_ordenado(n):
    v = list(range(n))
    qtd_trocas = int(n * 0.005)
    crand = CRand(42)
    for _ in range(qtd_trocas):
        r1 = crand.rand()
        r2 = crand.rand()
        idx1 = ((r1 << 15) | r2) % n
        idx2 = idx1 - 1 if idx1 == n - 1 else idx1 + 1
        v[idx1], v[idx2] = v[idx2], v[idx1]
    return v

# Implementações dos algoritmos de ordenação em Python (Fallback)
def bubble_sort_py(v):
    comparacoes = 0
    trocas = 0
    n = len(v)
    k = n
    while k > 0:
        ultima_troca = 0
        for i in range(k - 1):
            comparacoes += 1
            if v[i] > v[i + 1]:
                v[i], v[i + 1] = v[i + 1], v[i]
                trocas += 1
                ultima_troca = i + 1
        k = ultima_troca
    return comparacoes, trocas

def insertion_sort_py(v):
    comparacoes = 0
    trocas = 0
    n = len(v)
    for i in range(1, n):
        chave = v[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if v[j] > chave:
                v[j + 1] = v[j]
                trocas += 1
                j -= 1
            else:
                break
        v[j + 1] = chave
    return comparacoes, trocas

def selection_sort_py(v):
    comparacoes = 0
    trocas = 0
    n = len(v)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if v[j] < v[min_idx]:
                min_idx = j
        if min_idx != i:
            v[i], v[min_idx] = v[min_idx], v[i]
            trocas += 1
    return comparacoes, trocas

def heap_sort_py(v):
    comparacoes = 0
    trocas = 0
    
    def max_heapify(n, i):
        nonlocal comparacoes, trocas
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2
        
        if esquerda < n:
            comparacoes += 1
            if v[esquerda] > v[maior]:
                maior = esquerda
                
        if direita < n:
            comparacoes += 1
            if v[direita] > v[maior]:
                maior = direita
                
        if maior != i:
            v[i], v[maior] = v[maior], v[i]
            trocas += 1
            max_heapify(n, maior)
            
    n = len(v)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(n, i)
        
    for i in range(n - 1, 0, -1):
        v[0], v[i] = v[i], v[0]
        trocas += 1
        max_heapify(i, 0)
        
    return comparacoes, trocas

def quick_sort_py(v):
    comparacoes = 0
    trocas = 0
    
    def particionar(baixo, alto):
        nonlocal comparacoes, trocas
        pivo = v[alto]
        i = baixo - 1
        for j in range(baixo, alto):
            comparacoes += 1
            if v[j] < pivo:
                i += 1
                v[i], v[j] = v[j], v[i]
                trocas += 1
        v[i + 1], v[alto] = v[alto], v[i + 1]
        trocas += 1
        return i + 1
        
    def quick_recursivo(baixo, alto):
        if baixo < alto:
            pi = particionar(baixo, alto)
            quick_recursivo(baixo, pi - 1)
            quick_recursivo(pi + 1, alto)
            
    quick_recursivo(0, len(v) - 1)
    return comparacoes, trocas

def shell_sort_py(v):
    comparacoes = 0
    trocas = 0
    n = len(v)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = v[i]
            j = i
            while j >= gap:
                comparacoes += 1
                if v[j - gap] > temp:
                    v[j] = v[j - gap]
                    trocas += 1
                    j -= gap
                else:
                    break
            v[j] = temp
        gap //= 2
    return comparacoes, trocas

def encontrar_gcc():
    # 1. Verifica se 'gcc' já está no PATH
    gcc_path = shutil.which("gcc")
    if gcc_path:
        return gcc_path
    
    # 2. Se for Windows, procura em caminhos comuns de instalação
    if sys.platform == "win32":
        caminhos_comuns = [
            r"C:\msys64\mingw64\bin\gcc.exe",
            r"C:\msys64\ucrt64\bin\gcc.exe",
            r"C:\msys64\clang64\bin\gcc.exe",
            r"C:\msys64\usr\bin\gcc.exe",
            r"C:\MinGW\bin\gcc.exe",
        ]
        for caminho in caminhos_comuns:
            if os.path.exists(caminho):
                return caminho
                
    return None

def compilar_projeto(gcc_path):
    log_info(f"Usando compilador: {gcc_path}")
    os.makedirs("bin", exist_ok=True)
    
    algoritmos = ["bubblesort", "heapsort", "insertionsort", "quicksort", "selectionsort", "shellsort"]
    ext = ".exe" if sys.platform == "win32" else ""
    cflags = ["-Wall", "-Wextra", "-O3", "-std=gnu99"]
    ldflags = []
    
    if sys.platform == "win32":
        ldflags.append("-Wl,--stack,67108864")
        
    for alg in algoritmos:
        saida = os.path.join("bin", f"{alg}{ext}")
        src_alg_c = os.path.join("src", alg, f"{alg}.c")
        src_main_c = os.path.join("src", alg, f"main.c")
        src_ordenacao_c = os.path.join("src", "ordenacao.c")
        
        cmd = [gcc_path] + cflags + [src_main_c, src_alg_c, src_ordenacao_c] + ldflags + ["-o", saida, "-lm"]
        
        log_info(f"Compilando {alg}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            log_erro(f"Falha ao compilar {alg}:")
            print(res.stderr)
            sys.exit(1)
            
    log_sucesso("Todos os algoritmos foram compilados com sucesso!")

def executar_binario(alg, args):
    ext = ".exe" if sys.platform == "win32" else ""
    caminho_bin = os.path.join("bin", f"{alg}{ext}")
    cmd = [caminho_bin] + [str(a) for a in args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        log_erro(f"Erro ao executar {alg}: {res.stderr}")
        sys.exit(1)
    return res.stdout.strip()

def rodar_py_bench(alg, N, cenario_id):
    # Seleciona o gerador de vetor
    if cenario_id == 1:
        v = gerar_vetor_aleatorio(N)
    elif cenario_id == 2:
        v = gerar_vetor_ordenado(N)
    elif cenario_id == 3:
        v = gerar_vetor_inverso(N)
    elif cenario_id == 4:
        v = gerar_vetor_quase_ordenado(N)
        
    # Seleciona a função de ordenação
    func_map = {
        "bubblesort": bubble_sort_py,
        "insertionsort": insertion_sort_py,
        "selectionsort": selection_sort_py,
        "heapsort": heap_sort_py,
        "quicksort": quick_sort_py,
        "shellsort": shell_sort_py
    }
    
    t_inicio = time.perf_counter()
    comp, trocas = func_map[alg](v)
    t_fim = time.perf_counter()
    
    tempo = t_fim - t_inicio
    return tempo, comp, trocas

def rodar_problema2_py(alg, N):
    tempos = []
    comp_total = 0
    trocas_total = 0
    for _ in range(10):
        # Gera vetor ordenado
        v = gerar_vetor_ordenado(N)
        t_inicio = time.perf_counter()
        if alg == "heapsort":
            comp, trocas = heap_sort_py(v)
        else:
            comp, trocas = quick_sort_py(v)
        t_fim = time.perf_counter()
        tempos.append(t_fim - t_inicio)
        comp_total = comp
        trocas_total = trocas
        
    media = sum(tempos) / 10
    desvio = math.sqrt(sum((t - media) ** 2 for t in tempos) / 9.0)
    return media, desvio, comp_total, trocas_total

def gerar_grafico(heapsort_dados, quicksort_dados):
    try:
        import matplotlib.pyplot as plt
        
        log_info("Gerando gráfico para o Problema 2...")
        
        algoritmos = ['Heapsort', 'Quicksort']
        tempos_medios = [float(heapsort_dados['tempo']), float(quicksort_dados['tempo'])]
        desvios = [float(heapsort_dados['desvio']), float(quicksort_dados['desvio'])]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        cores_barras = ['#3498db', '#e74c3c']
        
        barras = ax.bar(algoritmos, tempos_medios, yerr=desvios, align='center', 
                        alpha=0.85, ecolor='black', capsize=10, color=cores_barras, width=0.5)
        
        ax.set_ylabel('Tempo Médio de Execução (segundos)', fontsize=12, fontweight='bold')
        ax.set_title('Problema 2: Tempo Médio de Execução (Ordenado, N=5000)\ncom Desvio Padrão', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.yaxis.grid(True, linestyle='--', alpha=0.6)
        
        for bar in barras:
            height = bar.get_height()
            ax.annotate(f'{height:.6f} s',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
                        
        plt.tight_layout()
        os.makedirs("data", exist_ok=True)
        plt.savefig(os.path.join("data", "grafico_problema_2.png"), dpi=300)
        plt.close()
        log_sucesso("Gráfico salvo com sucesso em 'data/grafico_problema_2.png'")
        
    except ImportError:
        log_aviso("Matplotlib não está instalado. Pulando a geração do gráfico de barras para o Problema 2.")
        log_aviso("Você pode instalar o Matplotlib rodando: pip install matplotlib")

def main():
    print(f"{Cores.NEGRITO}=================================================================={Cores.FIM}")
    print(f"{Cores.NEGRITO}   Automação dos Experimentos de Algoritmos de Ordenação{Cores.FIM}")
    print(f"{Cores.NEGRITO}=================================================================={Cores.FIM}")
    
    # 1. Tenta encontrar compilador
    gcc_path = encontrar_gcc()
    usar_fallback = False
    
    if gcc_path:
        log_info(f"GCC encontrado em: {gcc_path}")
        compilar_projeto(gcc_path)
    else:
        log_aviso("Compilador GCC não encontrado!")
        log_info("Executando a simulação de benchmarks em PYTHON NATIVO (Fallback).")
        log_info("Nota: As métricas de comparações/trocas serão IDENTICAS ao C, mas os tempos de CPU serão maiores.")
        usar_fallback = True
        
    # Prepara pasta de dados
    os.makedirs("data", exist_ok=True)
    resultados_gerais_path = os.path.join("data", "resultados_gerais.csv")
    
    # Limpa ou cria arquivo de resultados gerais
    with open(resultados_gerais_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo_ou_Media", "DesvioPadrao_ou_Comparacoes", "Comparacoes_ou_Trocas", "Trocas_Se_Media"])
        
    linhas_csv = []
    
    # -------------------------------------------------------------
    # PROBLEMA 1
    # -------------------------------------------------------------
    log_info("Executando Problema 1 (N = 30000)...")
    prob1_algs = ["bubblesort", "insertionsort", "selectionsort"]
    cenarios_nome = {1: "Aleatorio", 2: "Ordenado", 3: "Inverso"}
    
    tabela_prob1 = []
    for alg in prob1_algs:
        for c_id in [1, 2, 3]:
            cen = cenarios_nome[c_id]
            log_info(f"  -> Rodando {alg} no cenário {cen}...")
            
            if usar_fallback:
                # Se for pior caso de bubble/insertion/selection em Python, pode demorar alguns segundos.
                # Exibimos aviso para acalmar o usuário.
                if c_id in [1, 3] and alg in ["bubblesort", "insertionsort", "selectionsort"]:
                    log_info(f"     (Aguarde, executando ordenação O(N^2) em Python para N=30000...)")
                tempo, comp, trocas = rodar_py_bench(alg, 30000, c_id)
                nome_alg = alg.capitalize()
            else:
                output = executar_binario(alg, [30000, c_id])
                parts = output.split(",")
                nome_alg, cen, tempo, comp, trocas = parts[0], parts[1], float(parts[2]), int(parts[3]), int(parts[4])
                
            tabela_prob1.append([nome_alg, cen, str(tempo), str(comp), str(trocas)])
            linhas_csv.append([nome_alg, cen, str(tempo), str(comp), str(trocas), ""])
            
    # Salva tabela do problema 1
    tabela_prob1_path = os.path.join("data", "tabela_problema_1.csv")
    with open(tabela_prob1_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo (s)", "Comparacoes", "Trocas"])
        writer.writerows(tabela_prob1)
    log_sucesso("Resultados do Problema 1 salvos em 'data/tabela_problema_1.csv'")
    
    # -------------------------------------------------------------
    # PROBLEMA 2
    # -------------------------------------------------------------
    log_info("Executando Problema 2 (N = 5000, 10 execuções)...")
    prob2_dados = {}
    for alg in ["heapsort", "quicksort"]:
        log_info(f"  -> Rodando {alg}...")
        
        if usar_fallback:
            media_t, desvio, comp, trocas = rodar_problema2_py(alg, 5000)
            nome_alg = alg.capitalize()
            cen_label = "Ordenado (Media)"
        else:
            output = executar_binario(alg, [5000])
            parts = output.split(",")
            nome_alg, cen_label, media_t, desvio, comp, trocas = parts[0], parts[1], float(parts[2]), float(parts[3]), int(parts[4]), int(parts[5])
            
        prob2_dados[alg] = {
            'tempo': str(media_t),
            'desvio': str(desvio),
            'comparacoes': str(comp),
            'trocas': str(trocas)
        }
        linhas_csv.append([nome_alg, cen_label, str(media_t), str(desvio), str(comp), str(trocas)])
        
    # Salva tabela do problema 2
    tabela_prob2_path = os.path.join("data", "tabela_problema_2.csv")
    with open(tabela_prob2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo Medio (s)", "Desvio Padrao (s)", "Comparacoes", "Trocas"])
        for alg, d in prob2_dados.items():
            writer.writerow([alg.capitalize(), "Ordenado", d['tempo'], d['desvio'], d['comparacoes'], d['trocas']])
    log_sucesso("Resultados do Problema 2 salvos em 'data/tabela_problema_2.csv'")
    
    # Gera o gráfico
    if 'heapsort' in prob2_dados and 'quicksort' in prob2_dados:
        gerar_grafico(prob2_dados['heapsort'], prob2_dados['quicksort'])
        
    # -------------------------------------------------------------
    # PROBLEMA 3
    # -------------------------------------------------------------
    log_info("Executando Problema 3 (N = 50000, Quase Ordenado)...")
    tabela_prob3 = []
    
    # Para insertionsort
    log_info("  -> Rodando insertionsort...")
    if usar_fallback:
        tempo, comp, trocas = rodar_py_bench("insertionsort", 50000, 4)
        nome_alg = "Insertionsort"
        cen = "Quase Ordenado"
    else:
        out_ins = executar_binario("insertionsort", [50000, 4])
        parts = out_ins.split(",")
        nome_alg, cen, tempo, comp, trocas = parts[0], parts[1], float(parts[2]), int(parts[3]), int(parts[4])
        
    tabela_prob3.append([nome_alg, cen, str(tempo), str(comp), str(trocas)])
    linhas_csv.append([nome_alg, cen, str(tempo), str(comp), str(trocas), ""])
    
    # Para shellsort
    log_info("  -> Rodando shellsort...")
    if usar_fallback:
        tempo, comp, trocas = rodar_py_bench("shellsort", 50000, 4)
        nome_alg = "Shellsort"
        cen = "Quase Ordenado"
    else:
        out_sh = executar_binario("shellsort", [50000])
        parts = out_sh.split(",")
        nome_alg, cen, tempo, comp, trocas = parts[0], parts[1], float(parts[2]), int(parts[3]), int(parts[4])
        
    tabela_prob3.append([nome_alg, cen, str(tempo), str(comp), str(trocas)])
    linhas_csv.append([nome_alg, cen, str(tempo), str(comp), str(trocas), ""])
    
    # Salva tabela do problema 3
    tabela_prob3_path = os.path.join("data", "tabela_problema_3.csv")
    with open(tabela_prob3_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Cenario", "Tempo (s)", "Comparacoes", "Trocas"])
        writer.writerows(tabela_prob3)
    log_sucesso("Resultados do Problema 3 salvos em 'data/tabela_problema_3.csv'")
    
    # -------------------------------------------------------------
    # SALVA RESULTADOS GERAIS
    # -------------------------------------------------------------
    with open(resultados_gerais_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(linhas_csv)
    log_sucesso("Todos os resultados brutos foram consolidados em 'data/resultados_gerais.csv'")
    
    # -------------------------------------------------------------
    # EXIBE RESUMO NO CONSOLE
    # -------------------------------------------------------------
    print(f"\n{Cores.NEGRITO}=================================================================={Cores.FIM}")
    print(f"{Cores.NEGRITO}                       RESUMO DOS RESULTADOS                      {Cores.FIM}")
    print(f"{Cores.NEGRITO}=================================================================={Cores.FIM}")
    
    print(f"\n{Cores.NEGRITO}Problema 1: Custo Teórico vs. Tempo Real (N = 30.000){Cores.FIM}")
    print(f"{'Algoritmo':<15} | {'Cenário':<12} | {'Tempo (s)':<10} | {'Comparações':<12} | {'Trocas':<12}")
    print("-" * 71)
    for row in tabela_prob1:
        print(f"{row[0]:<15} | {row[1]:<12} | {float(row[2]):<10.6f} | {int(row[3]):<12} | {int(row[4]):<12}")
        
    print(f"\n{Cores.NEGRITO}Problema 2: Heapsort vs. Quicksort Clássico (N = 5.000, 10 execs, Ordenado){Cores.FIM}")
    print(f"{'Algoritmo':<15} | {'Tempo Médio (s)':<16} | {'Desvio Padrão':<14} | {'Comparações':<12} | {'Trocas':<12}")
    print("-" * 77)
    for alg, d in prob2_dados.items():
        print(f"{alg.capitalize():<15} | {float(d['tempo']):<16.6f} | {float(d['desvio']):<14.6f} | {int(d['comparacoes']):<12} | {int(d['trocas']):<12}")
        
    print(f"\n{Cores.NEGRITO}Problema 3: Vetores Quase Ordenados (N = 50.000, Quase Ordenado){Cores.FIM}")
    print(f"{'Algoritmo':<15} | {'Cenário':<15} | {'Tempo (s)':<10} | {'Comparações':<12} | {'Trocas':<12}")
    print("-" * 74)
    for row in tabela_prob3:
        print(f"{row[0]:<15} | {row[1]:<15} | {float(row[2]):<10.6f} | {int(row[3]):<12} | {int(row[4]):<12}")
        
    print(f"\n{Cores.NEGRITO}=================================================================={Cores.FIM}")
    log_sucesso("Processo finalizado com sucesso! Todos os dados e gráficos estão na pasta 'data/'.")
    print(f"{Cores.NEGRITO}=================================================================={Cores.FIM}")

if __name__ == "__main__":
    main()
