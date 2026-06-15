#ifndef ORDENACAO_H
#define ORDENACAO_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    unsigned long long comparacoes;
    unsigned long long trocas;
    double tempo_segundos;
} Metricas;

// Apenas os protótipos (sem static inline)
void gerarVetorAleatorio(int *v, int n);
void gerarVetorOrdenado(int *v, int n);
void gerarVetorInverso(int *v, int n);
void gerarVetorQuaseOrdenado(int *v, int n);

#endif