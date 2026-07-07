#include "insertionsort.h"

void InsertionSort(int* vetor, int n, Metricas* m) {
  m->comparacoes = 0;
  m->trocas = 0;

  for (int i = 1; i < n; i++) {
    int chave = vetor[i];
    int j = i - 1;

    while (j >= 0) {
      m->comparacoes++;
      if (vetor[j] > chave) {
        vetor[j + 1] = vetor[j];
        m->trocas++;
        j--;
      } else {
        break;
      }
    }
    vetor[j + 1] = chave;
  }
}