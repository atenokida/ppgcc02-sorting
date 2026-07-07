// Cabeçalho de funções auxiliares utilizadas nos experimentos (i.e., problemas 1-3).

#ifndef SORTING_ORDENACAO_H_
#define SORTING_ORDENACAO_H_

static const char kOutputPath[] = "./data/output.csv";

typedef struct Metricas {
  unsigned long long comparacoes;
  unsigned long long trocas;
  double tempo_segundos;
} Metricas;

// Estratégia de população do vetor.
enum Estrategia {
  kAleatorio = 0,
  kOrdenadoCrescente = 1,
  kOrdenadoDecrescente = 2,
  kParcialmenteOrdenado = 3
};

enum Algoritmo {
  kBubbleSort = 0,
  kHeapSort = 1,
  kInsertionSort = 2,
  kQuickSort = 3,
  kSelectionSort = 4,
  kShellSort = 5
};

void GerarVetorAleatorio(int* v, int n);
void GerarVetorOrdenado(int* v, int n);
void GerarVetorInverso(int* v, int n);
void GerarVetorQuaseOrdenado(int* v, int n);

void ExecutarExperimento(
    const int num_elementos, 
    const enum Estrategia estrategia, 
    const enum Algoritmo* algoritmos, 
    const int tam_algoritmos, 
    const char* nome_experimento, 
    const int execucoes);

#endif