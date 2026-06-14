#include "insertionsort.h"

void rodar_experimento(int c, int n, int e) {
    int *vetor = (int *)malloc(n * sizeof(int));
    srand(42);
    
    if(e == 1) { // Problema 1
        if(c == 1) gerarVetorAleatorio(vetor, n);
        if(c == 2) gerarVetorOrdenado(vetor, n);
        if(c == 3) gerarVetorInverso(vetor, n);
    } else {     // Problema 3
        gerarVetorQuaseOrdenado(vetor, n);
    }

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    insertionSort(vetor, n, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Config [%d] -> Tempo: %f s | Comp: %llu | Trocas: %llu\n", c, m.tempo_segundos, m.comparacoes, m.trocas);
    free(vetor);
}

int main() {
    printf("--- INSERTION SORT EXP 1 (N=30000) ---\n");
    rodar_experimento(1, 30000, 1);
    rodar_experimento(2, 30000, 1);
    rodar_experimento(3, 30000, 1);
    
    printf("\n--- INSERTION SORT EXP 3 (N=50000 Quase Ord.) ---\n");
    rodar_experimento(4, 50000, 3);
    return 0;
}