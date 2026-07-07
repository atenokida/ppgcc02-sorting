CC       := gcc
# A flag -I./include é essencial para encontrar os cabeçalhos (.h)
CFLAGS   := -Wall -Wextra -O3 -std=gnu99 -I./include
LIBS     := -lm

# Aumenta a pilha nativamente se a compilação for no Windows
ifeq ($(OS),Windows_NT)
    LDFLAGS := -Wl,--stack,67108864
else
    LDFLAGS :=
endif

SRC_DIR  := .
BIN_DIR  := ../bin
DATA_DIR := ../data

# Define o nome do executável final
EXEC := $(BIN_DIR)/programa

# Lista de todos os códigos-fonte necessários para o main central
SRCS := $(SRC_DIR)/main.c \
        $(SRC_DIR)/ordenacao/ordenacao.c \
        $(SRC_DIR)/bubblesort/bubblesort.c \
        $(SRC_DIR)/heapsort/heapsort.c \
        $(SRC_DIR)/insertionsort/insertionsort.c \
        $(SRC_DIR)/quicksort/quicksort.c \
        $(SRC_DIR)/selectionsort/selectionsort.c \
        $(SRC_DIR)/shellsort/shellsort.c

.PHONY: all clean run

all: $(BIN_DIR) $(DATA_DIR) $(EXEC)
	@echo "=================================================================="
	@echo " Compilação concluída! Executável gerado em '$(EXEC)'"
	@echo "=================================================================="

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

$(DATA_DIR):
	@mkdir -p $(DATA_DIR)

# Regra para compilar o executável central unindo todos os .c
$(EXEC): $(SRCS)
	@echo "Compilando o projeto unificado..."
	@$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

clean:
	@echo "Limpando os binários executáveis e os dados gerados..."
	@rm -rf $(BIN_DIR)
	@echo "Projeto limpo com sucesso!"

run: all
	@echo "Aumentando o limite da pilha de execução (Linux/Mac)..."
	@ulimit -s unlimited 2>/dev/null || true
	@echo "Executando todos os experimentos..."
	@# O comando cd garante que o executável rode a partir da raiz 
	@# ou da pasta correta caso use caminhos relativos para os arquivos .csv
	@cd .. && ./bin/programa
	@echo "Finalizado! Verifique a pasta data/ para ver os arquivos gerados."