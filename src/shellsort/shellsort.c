#include "shellsort.h"

void ShellSort(int* vetor, int n, Metricas* m) {
  m->comparacoes = 0;
  m->trocas = 0;

  for (int gap = n / 2; gap > 0; gap /= 2) {
    for (int i = gap; i < n; i++) {
      int temp = vetor[i];
      int j = i;

      while (j >= gap) {
        m->comparacoes++;
        if (vetor[j - gap] > temp) {
          vetor[j] = vetor[j - gap];
          m->trocas++;
          j -= gap;
        } else {
          break;
        }
      }
      vetor[j] = temp;
    }
  }
}