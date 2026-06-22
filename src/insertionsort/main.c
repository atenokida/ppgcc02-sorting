#include "insertionsort.h"

void rodar_experimento(int c, int n, int e) {
    int *vetor = (int *)malloc(n * sizeof(int));
    srand(42);
    char *nome_cenario;
    
    if(e == 1) { // Problema 1
        if(c == 1) { gerarVetorAleatorio(vetor, n); nome_cenario = "Aleatorio"; }
        else if(c == 2) { gerarVetorOrdenado(vetor, n); nome_cenario = "Ordenado"; }
        else { gerarVetorInverso(vetor, n); nome_cenario = "Inverso"; }
    } else {     // Problema 3
        gerarVetorQuaseOrdenado(vetor, n);
        nome_cenario = "Quase Ordenado";
    }

    struct timespec inicio, fim;
    Metricas m;

    clock_gettime(CLOCK_MONOTONIC, &inicio);
    insertionSort(vetor, n, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
    printf("Insertionsort,%s,%f,%llu,%llu\n", nome_cenario, m.tempo_segundos, m.comparacoes, m.trocas);
    free(vetor);
}

int main() {
    rodar_experimento(1, 30000, 1);
    rodar_experimento(2, 30000, 1);
    rodar_experimento(3, 30000, 1);
    
    rodar_experimento(4, 50000, 3);
    return 0;
}