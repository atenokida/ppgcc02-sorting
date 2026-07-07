#include "quicksort.h"

static int Particionar(int* vetor, int baixo, int alto, Metricas* m) {
  int pivo = vetor[alto];
  int i = (baixo - 1);

  for (int j = baixo; j <= alto - 1; j++) {
    m->comparacoes++;
    if (vetor[j] < pivo) {
      i++;
      int temp = vetor[i];
      vetor[i] = vetor[j];
      vetor[j] = temp;
      m->trocas++;
    }
  }
  int temp = vetor[i + 1];
  vetor[i + 1] = vetor[alto];
  vetor[alto] = temp;
  m->trocas++;

  return (i + 1);
}

static void QuickRecursivo(int* vetor, int baixo, int alto, Metricas* m) {
  if (baixo < alto) {
    int pi = Particionar(vetor, baixo, alto, m);
    QuickRecursivo(vetor, baixo, pi - 1, m);
    QuickRecursivo(vetor, pi + 1, alto, m);
  }
}

void QuickSort(int *vetor, int n, Metricas *m) {
  m->comparacoes = 0;
  m->trocas = 0;
  QuickRecursivo(vetor, 0, n - 1, m);
}