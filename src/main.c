#include "bubblesort.h"
#include "heapsort.h"
#include "insertionsort.h"
#include "ordenacao.h"
#include "quicksort.h"
#include "selectionsort.h"
#include "shellsort.h"

// No problema 1 testamos os algoritmos de custo quadrático
// com 30 K elementos em três instâncias: aleatória (na especificação
// está como uniforme), ordenada crescente e ordenada decrescente.
void Problema1() {
  int n = 30000;
  int execucoes = 1;
  enum Estrategia estrategias[] = { kAleatorio, kOrdenadoCrescente, kOrdenadoDecrescente };
  enum Algoritmo algoritmos[] = { kBubbleSort, kInsertionSort, kSelectionSort };

  for (int i = 0; i < 3; i++) {
    ExecutarExperimento(n, estrategias[i], algoritmos, 3, "problema_1", execucoes);
  }
}

// O problema 2 compara o desempenho do quicksort e heapsort
// em um vetor ordenado crescentemente de tamanho 5.000 sobre 10 execuções.
void Problema2() {
  int n = 5000;
  int execucoes = 10;
  enum Algoritmo algoritmos[] = { kHeapSort, kQuickSort };

  ExecutarExperimento(n, kOrdenadoCrescente, algoritmos, 2, "problema_2", execucoes);
}

// O problema 3 compara o insertionsort e shellsort em um vetor
// parcialmente ordenado (5% do total) de tamanho 50.000.
void Problema3() {
  int n = 50000;
  int execucoes = 1;
  enum Algoritmo algoritmos[] = { kInsertionSort, kShellSort };

  ExecutarExperimento(n, kParcialmenteOrdenado, algoritmos, 2, "problema_3", execucoes);
}

int main() {
  Problema1();
  Problema2();
  Problema3();

  return 0;
}