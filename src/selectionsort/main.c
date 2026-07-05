#include "selectionsort.h"

void rodar_experimento(int c, int N) {
    int *vetor = (int *)malloc(N * sizeof(int));
    if (vetor == NULL) return;
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

int main(int argc, char *argv[]) {
    int N = 30000;
    if (argc > 1) {
        N = atoi(argv[1]);
    }
    
    if (argc > 2) {
        int c = atoi(argv[2]);
        if (c >= 1 && c <= 3) {
            rodar_experimento(c, N);
        }
    } else {
        rodar_experimento(1, N);
        rodar_experimento(2, N);
        rodar_experimento(3, N);
    }
    return 0;
}