#include "heapsort.h"
#include <math.h>

int main(int argc, char *argv[]) {
    int N = 5000;
    if (argc > 1) {
        N = atoi(argv[1]);
    }
    double tempos[10];
    double soma = 0, media = 0, desvio = 0;
    Metricas m_total = {0, 0, 0};

    for (int i = 0; i < 10; i++) {
        int *vetor = (int *)malloc(N * sizeof(int));
        if (vetor == NULL) {
            fprintf(stderr, "Erro de alocação de memória.\n");
            return 1;
        }
        gerarVetorOrdenado(vetor, N);

        struct timespec inicio, fim;
        Metricas m;

        clock_gettime(CLOCK_MONOTONIC, &inicio);
        heapSort(vetor, N, &m);
        clock_gettime(CLOCK_MONOTONIC, &fim);

        tempos[i] = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
        soma += tempos[i];
        m_total.comparacoes = m.comparacoes;
        m_total.trocas = m.trocas;
        
        free(vetor);
    }

    media = soma / 10;
    for (int i = 0; i < 10; i++) {
        desvio += pow(tempos[i] - media, 2);
    }
    desvio = sqrt(desvio / 9.0);

    // Formato CSV para o Problema 2: Algoritmo,Cenario,TempoMedio,DesvioPadrao,Comparacoes,Trocas
    printf("Heapsort,Ordenado (Media),%f,%f,%llu,%llu\n", media, desvio, m_total.comparacoes, m_total.trocas);

    return 0;
}