#include "selectionsort.h"

void SelectionSort(int* vetor, int n, Metricas* m) {
  m->comparacoes = 0;
  m->trocas = 0;

  for (int i = 0; i < n - 1; i++) {
    int min_idx = i;
    for (int j = i + 1; j < n; j++) {
      m->comparacoes++;
      if (vetor[j] < vetor[min_idx]) {
        min_idx = j;
      }
    }

    if (min_idx != i) {
      int temp = vetor[min_idx];
      vetor[min_idx] = vetor[i];
      vetor[i] = temp;
      m->trocas++;
    }
  }
}