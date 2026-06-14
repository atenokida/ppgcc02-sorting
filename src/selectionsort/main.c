#include "selectionsort.h"

void rodar_experimento(int c) {
    int N = 30000;
    int *vetor = (int *)malloc(N * sizeof(int));
    srand(42);
    
    if(c == 1) gerarVetorAleatorio(vetor, N);
    if(c == 2) gerarVetorOrdenado(vetor, N);
    if(c == 3) gerarVetorInverso(vetor, N);

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    selectionSort(vetor, N, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Cenario %d -> Tempo: %f s | Comp: %llu | Trocas: %llu\n", c, m.tempo_segundos, m.comparacoes, m.trocas);
    free(vetor);
}

int main() {
    printf("--- SELECTION SORT EXP 1 ---\n");
    rodar_experimento(1);
    rodar_experimento(2);
    rodar_experimento(3);
    return 0;
}