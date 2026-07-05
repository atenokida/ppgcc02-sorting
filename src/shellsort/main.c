#include "shellsort.h"

int main(int argc, char *argv[]) {
    int N = 50000;
    if (argc > 1) {
        N = atoi(argv[1]);
    }
    int *vetor = (int *)malloc(N * sizeof(int));
    if (vetor == NULL) {
        fprintf(stderr, "Erro de alocação de memória.\n");
        return 1;
    }
    srand(42);
    
    gerarVetorQuaseOrdenado(vetor, N);

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    shellSort(vetor, N, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Shellsort,Quase Ordenado,%f,%llu,%llu\n", m.tempo_segundos, m.comparacoes, m.trocas);
    
    free(vetor);
    return 0;
}