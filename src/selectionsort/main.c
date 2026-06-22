#include "selectionsort.h"

void rodar_experimento(int c) {
    int N = 30000;
    int *vetor = (int *)malloc(N * sizeof(int));
    srand(42);
    
    char *nome_cenario;
    if(c == 1) { gerarVetorAleatorio(vetor, N); nome_cenario = "Aleatorio"; }
    else if(c == 2) { gerarVetorOrdenado(vetor, N); nome_cenario = "Ordenado"; }
    else { gerarVetorInverso(vetor, N); nome_cenario = "Inverso"; }

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    selectionSort(vetor, N, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Selectionsort,%s,%f,%llu,%llu\n", nome_cenario, m.tempo_segundos, m.comparacoes, m.trocas);
    free(vetor);
}

int main() {
    rodar_experimento(1);
    rodar_experimento(2);
    rodar_experimento(3);
    return 0;
}