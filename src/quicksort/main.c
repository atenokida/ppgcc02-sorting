#include "quicksort.h"
#include <math.h>

int main() {
    int N = 5000;
    double tempos[10];
    double soma = 0, media = 0, desvio = 0;
    Metricas m_total = {0, 0, 0};

    for (int i = 0; i < 10; i++) {
        int *vetor = (int *)malloc(N * sizeof(int));
        gerarVetorOrdenado(vetor, N); 
        
        struct timespec inicio, fim;
        Metricas m;

        clock_gettime(CLOCK_MONOTONIC, &inicio);
        quickSort(vetor, N, &m);
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
    printf("Quicksort,Ordenado (Media),%f,%f,%llu,%llu\n", media, desvio, m_total.comparacoes, m_total.trocas);

    return 0;
}