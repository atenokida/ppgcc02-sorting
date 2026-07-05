CC       := gcc
CFLAGS   := -Wall -Wextra -O3 -std=gnu99
LIBS     := -lm

ifeq ($(OS),Windows_NT)
    LDFLAGS := -Wl,--stack,67108864
else
    LDFLAGS :=
endif

SRC_DIR  := .
BIN_DIR  := ../bin
DATA_DIR := ../data

ALGORITMOS := bubblesort heapsort insertionsort quicksort selectionsort shellsort

EXECUTABLES := $(addprefix $(BIN_DIR)/, $(ALGORITMOS))

all: $(BIN_DIR) $(EXECUTABLES)
	@echo "=================================================================="
	@echo " Todos os 6 algoritmos de ordenação foram compilados em '$(BIN_DIR)'!"
	@echo "=================================================================="

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

$(BIN_DIR)/%: $(SRC_DIR)/%/main.c $(SRC_DIR)/%/*.c $(SRC_DIR)/ordenacao.c
	@echo "Compilando o executável para: $*..."
	@$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

.PHONY: $(ALGORITMOS)
$(ALGORITMOS): $(BIN_DIR)
	@$(MAKE) $(BIN_DIR)/$@

.PHONY: clean
clean:
	@echo "Limpando os binários executáveis e os dados gerados..."
	@rm -rf $(BIN_DIR)
	@rm -rf $(DATA_DIR)
	@echo "Projeto limpo com sucesso!"

$(DATA_DIR):
	@mkdir -p $(DATA_DIR)

.PHONY: run
run: all $(DATA_DIR)
	@echo "Executando os algoritmos de ordenação e gerando o relatório..."
	@> $(DATA_DIR)/resultados_gerais.csv
	@for alg in $(ALGORITMOS); do \
		echo "Rodando $$alg..."; \
		$(BIN_DIR)/$$alg >> $(DATA_DIR)/resultados_gerais.csv; \
	done
	@echo "Finalizado! Verifique o arquivo $(DATA_DIR)/resultados_gerais.csv"