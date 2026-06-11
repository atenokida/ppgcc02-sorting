#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/sysinfo.h>
#include <stddef.h>

typedef struct {
    unsigned long long comparacoes;
    unsigned long long trocas;
    double tempo_segundos;
} Metricas;

void heapify(int arr[], int n, int i, Metricas* m)
{

    int largest = i;

    //index direita e esquerda
    int l = 2 * i + 1;
    int r = 2 * i + 2;

    //se esquerda for maior que a raiz, o maior vira a posição da esquerda
    m->comparacoes++;
    if (l < n && arr[l] > arr[largest])
        largest = l;

    //se direita é maior que o raiz, o maior vira o elemento da direita 
    m->comparacoes++;
    if (r < n && arr[r] > arr[largest])
        largest = r;

    m->comparacoes++;
    if (largest != i)
    {
        m->trocas++;
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest, m);
    }
}

void heapSort(int arr[], int n, Metricas* m)
{
    //constroi a arvore levando o maior elemento para raiz
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i, m);

    //troca a primeira e a ultima posicao livre e corrige a arvore
    for (int i = n - 1; i > 0; i--)
    {
        m->trocas++;
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify(arr, i, 0, m);
    }
}

void geraVetorAleatorio(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = rand() % 100000;
}

void gerarVetorOrdenado(int *v, int n) {
    for (int i = 0; i < n; i++) v[i] = i;
}


int main()
{
    srand(42);
    int arr[100];
    struct timespec inicio, fim;
    int n = sizeof(arr) / sizeof(arr[0]);//calcula o tamnho do array
    Metricas m;
    m.comparacoes = 0.0;
    m.trocas = 0.0;
    geraVetorAleatorio(arr, n);
    clock_gettime(CLOCK_MONOTONIC, &inicio);
    heapSort(arr, n, &m);
    clock_gettime(CLOCK_MONOTONIC, &fim);

    m.tempo_segundos = (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec)/ 1e9;
    for (int i = 0; i < n; ++i)
        printf("%d ", arr[i]);


    printf("Resultados:\nTempo: %f s\nComparacoes: %llu\nTrocas: %llu\n", m.tempo_segundos, m.comparacoes, m.trocas);
    return 0;
}