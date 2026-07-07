#include "ordenacao.h"

#include <time.h>  // timespec, clock_gettime, CLOCK_MONOTONIC, srand

#include <stdio.h>  // FILE, fopen, fclose, fprintf
#include <stdlib.h>  // malloc, rand
#include <string.h>  // memcpy

#include "bubblesort.h"
#include "heapsort.h"
#include "insertionsort.h"
#include "quicksort.h"
#include "selectionsort.h"
#include "shellsort.h"

void GerarVetorAleatorio(int* v, int n) {
  for (int i = 0; i < n; i++) v[i] = ((rand() << 15) | rand()) % 100000;
}

void GerarVetorOrdenado(int* v, int n) {
  for (int i = 0; i < n; i++) v[i] = i;
}

void GerarVetorInverso(int* v, int n) {
  for (int i = 0; i < n; i++) v[i] = n - i;
}

void GerarVetorQuaseOrdenado(int* v, int n) {
  for (int i = 0; i < n; i++) v[i] = i;
  int qtd_trocas = (int)(n * 0.05);
  for (int i = 0; i < qtd_trocas; i++) {
    int idx1 = ((rand() << 15) | rand()) % n;
    int idx2 = (idx1 == n - 1) ? idx1 - 1 : idx1 + 1;
    int temp = v[idx1];
    v[idx1] = v[idx2];
    v[idx2] = temp;
  }
}

void SalvarResultado(
    const char* nome_experimento, 
    const enum Algoritmo algoritmo, 
    const enum Estrategia estrategia,
    const int num_elementos,
    const struct Metricas metricas) {
  char* str_algoritmo = "undefined";
  char* str_estrategia = "undefined";

  switch (algoritmo) {
    case kBubbleSort:
      str_algoritmo = "BubbleSort";
      break;
    case kHeapSort:
      str_algoritmo = "HeapSort";
      break;
    case kInsertionSort:
      str_algoritmo = "InsertionSort";
      break;
    case kQuickSort:
      str_algoritmo = "QuickSort";
      break;
    case kSelectionSort:
      str_algoritmo = "SelectionSort";
      break;
    case kShellSort:
      str_algoritmo = "ShellSort";
      break;
  }
  switch (estrategia) {
    case kAleatorio:
      str_estrategia = "Aleatório";
      break;
    case kOrdenadoCrescente:
      str_estrategia = "OrdenadoCrescente";
      break;
    case kOrdenadoDecrescente:
      str_estrategia = "OrdenadoDecrescente";
      break;
    case kParcialmenteOrdenado:
      str_estrategia = "ParcialmenteOrdenado";
      break;
  }

  FILE* file = fopen(kOutputPath, "ab+");

  // Cabeçalho do arquivo de saída:
  // experimento,algoritmo,tamanho,vetor_entrada,num_comparacoes,num_trocas,tempo_execucao
  fprintf(file, "%s,%s,%d,%s,%lld,%lld,%.5f\n", 
          nome_experimento, 
          str_algoritmo, 
          num_elementos, 
          str_estrategia, 
          (long long)metricas.comparacoes, 
          (long long)metricas.trocas, 
          metricas.tempo_segundos);

  fclose(file);
}

void ExecutarExperimento(
    const int num_elementos, 
    const enum Estrategia estrategia, 
    const enum Algoritmo* algoritmos, 
    const int tam_algoritmos, 
    const char* nome_experimento, 
    const int execucoes) {
  int* vetor = (int*)malloc(sizeof(int) * num_elementos);
  // Vetor de entrada dos algoritmos.
  // Vamos utilizá-lo para evitar gerar o vetor aleatório múltiplas vezes.
  int* tmp = (int*)malloc(sizeof(int) * num_elementos);
  srand(42);
  
  switch (estrategia) {
    case kAleatorio:
      GerarVetorAleatorio(vetor, num_elementos);
      break;
    case kOrdenadoCrescente:
      GerarVetorOrdenado(vetor, num_elementos);
      break;
    case kOrdenadoDecrescente:
      GerarVetorInverso(vetor, num_elementos);
      break;
    case kParcialmenteOrdenado:
      GerarVetorQuaseOrdenado(vetor, num_elementos);
      break;
  }
  
  for (int i = 0; i < tam_algoritmos; i++) {
    for (int exec = 0; exec < execucoes; exec++) {
      memcpy(tmp, vetor, sizeof(int) * num_elementos);
      struct timespec inicio, fim;
      struct Metricas metricas;

      switch (algoritmos[i]) {
        case kBubbleSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          BubbleSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
        case kHeapSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          HeapSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
        case kInsertionSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          InsertionSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
        case kQuickSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          QuickSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
        case kSelectionSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          SelectionSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
        case kShellSort:
          clock_gettime(CLOCK_MONOTONIC, &inicio);
          ShellSort(tmp, num_elementos, &metricas);
          clock_gettime(CLOCK_MONOTONIC, &fim);
          metricas.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
          break;
      }

      SalvarResultado(nome_experimento, algoritmos[i], estrategia, num_elementos, metricas);
    }
  }
}