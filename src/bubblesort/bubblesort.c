#include "bubblesort.h"

void BubbleSort(int* vetor, int n, Metricas* m) {
  m->comparacoes = 0;
  m->trocas = 0;
  int k = n;

  while (k > 0) {
    int ultima_troca = 0;
    for (int i = 0; i < k - 1; i++) {
      m->comparacoes++;
      if (vetor[i] > vetor[i + 1]) {
        int temp = vetor[i];
        vetor[i] = vetor[i + 1];
        vetor[i + 1] = temp;

        m->trocas++;
        ultima_troca = i + 1;
      }
    }
    k = ultima_troca;
  }
}