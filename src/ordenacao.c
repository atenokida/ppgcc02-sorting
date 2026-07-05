#include "ordenacao.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void gerarVetorAleatorio(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = rand() % 100000;
}

void gerarVetorOrdenado(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = i;
}

void gerarVetorInverso(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = n - i;
}

void gerarVetorQuaseOrdenado(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = i;
    int qtd_trocas = (int)(n * 0.005);
    for (int i = 0; i < qtd_trocas; i++) {
        int idx1 = rand() % n;
        int idx2 = (idx1 == n - 1) ? idx1 - 1 : idx1 + 1; 
        int temp = v[idx1];
        v[idx1] = v[idx2];
        v[idx2] = temp;
    }
}

