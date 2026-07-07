#include "heapsort.h"

static void MaxHeapify(int* vetor, int n, int i, Metricas* m) {
  int maior = i;
  int esquerda = 2 * i + 1;
  int direita = 2 * i + 2;

  if (esquerda < n) {
    m->comparacoes++;
    if (vetor[esquerda] > vetor[maior]) maior = esquerda;
  }

  if (direita < n) {
    m->comparacoes++;
    if (vetor[direita] > vetor[maior]) maior = direita;
  }

  if (maior != i) {
    int troca = vetor[i];
    vetor[i] = vetor[maior];
    vetor[maior] = troca;
    m->trocas++;

    MaxHeapify(vetor, n, maior, m);
  }
}

void HeapSort(int* vetor, int n, Metricas* m) {
  m->comparacoes = 0;
  m->trocas = 0;

  for (int i = n / 2 - 1; i >= 0; i--) {
    MaxHeapify(vetor, n, i, m);
  }

  for (int i = n - 1; i > 0; i--) {
    int temp = vetor[0];
    vetor[0] = vetor[i];
    vetor[i] = temp;
    m->trocas++;

    MaxHeapify(vetor, i, 0, m);
  }
}