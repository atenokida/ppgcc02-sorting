#include "shellsort.h"

int main() {
    printf("--- SHELL SORT EXP 3 (N=50000 Quase Ord.) ---\n");
    int N = 50000;
    int *vetor = (int *)malloc(N * sizeof(int));
    srand(42);
    
    gerarVetorQuaseOrdenado(vetor, N);

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    shellSort(vetor, N, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Shellsort -> Tempo: %f s | Comp: %llu | Trocas: %llu\n", m.tempo_segundos, m.comparacoes, m.trocas);
    
    free(vetor);
    return 0;
}