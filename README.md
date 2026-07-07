# Análise de Algoritmos de Ordenação

Este projeto consiste na implementação, compilação e análise de desempenho de seis algoritmos de ordenação clássicos na linguagem C. O objetivo é avaliar o comportamento de cada método em diferentes cenários de entrada (aleatório, ordenado, inverso e quase ordenado).

Os experimentos e tempos de execução registrados no relatório foram obtidos no seguinte ambiente de execução:
* **Processador (CPU):** AMD Ryzen 5 5500 (6 Cores / 12 Threads)
* **Memória RAM:** 16 GB DDR4 @ 3200 MHz
* **Sistema Operacional:** CachyOS (Linux)
---

## Estrutura do Repositório

* **`/src`**: Contém o código-fonte do projeto, incluindo o `Makefile`, os arquivos compartilhados (`ordenacao.c` e `ordenacao.h`), e uma pasta para cada algoritmo.
* **`/data`**: Pasta onde são salvos os relatórios gerados em formato `.csv` e gráficos de desempenho.
* **`/bin`**: Diretório criado automaticamente durante a compilação para armazenar os arquivos executáveis.

---

## Como Compilar o Projeto

Todas as operações de compilação devem ser executadas a partir da pasta **`src`**. Navegue até ela antes de rodar os comandos:

```bash
cd src

```

### 1. Compilar Todos os Algoritmos

Para compilar os 6 algoritmos de uma única vez, utilize o comando padrão:

```bash
make

```

*(Os executáveis serão gerados na pasta `../bin`)*

### 2. Compilar um Algoritmo Específico

Se desejar compilar apenas um dos métodos, use `make` seguido do nome do algoritmo em minúsculo:

```bash
make bubblesort
make heapsort
make insertionsort
make quicksort
make selectionsort
make shellsort

```

### 3. Limpar os Arquivos Gerados

Para remover todos os binários da pasta `bin` e os dados gerados na pasta `data`, execute:

```bash
make clean

```

---

## 🏃 Como Executar os Algoritmos

### Execução Individual (Manual)

Caso queira testar um algoritmo isoladamente após a compilação, você deve chamar o binário correspondente a partir da raiz do projeto ou da pasta `bin`:

```bash
./bin/bubblesort
./bin/heapsort
./bin/insertionsort
./bin/quicksort
./bin/selectionsort
./bin/shellsort

```

> **Nota Importante sobre o Quicksort:** Em cenários de vetores já ordenados (caso degenerado), o Quicksort clássico pode sofrer estouro de pilha (*Stack Overflow*) devido à profundidade da recursão. Se notar que o programa travou ou fechou abruptamente, execute o comando abaixo no terminal antes de rodar o executável:

> ```bash
> ulimit -s unlimited
> 
> ```