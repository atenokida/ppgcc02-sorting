CC       := gcc
CFLAGS   := -Wall -Wextra -O3 -std=gnu99
LIBS     := -lm

SRC_DIR  := .
BIN_DIR  := ../bin

ALGORITMOS := bubblesort heapsort insertionsort quicksort selectionsort shellsort

EXECUTABLES := $(addprefix $(BIN_DIR)/, $(ALGORITMOS))

all: $(BIN_DIR) $(EXECUTABLES)
	@echo "=================================================================="
	@echo " Todos os 6 algoritmos de ordenação foram compilados em '$(BIN_DIR)'!"
	@echo "=================================================================="

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

$(BIN_DIR)/%: $(SRC_DIR)/%/main.c $(SRC_DIR)/%/%..c $(SRC_DIR)/ordenacao.c
	@echo "Compilando o executável para: $*..."
	@$(CC) $(CFLAGS) $^ -o $@ $(LIBS)

$(BIN_DIR)/%: $(SRC_DIR)/%/main.c $(SRC_DIR)/%/*.c $(SRC_DIR)/ordenacao.c
	@echo "Compilando o executável para: $*..."
	@$(CC) $(CFLAGS) $^ -o $@ $(LIBS)

.PHONY: $(ALGORITMOS)
$(ALGORITMOS): $(BIN_DIR)
	@$(MAKE) $(BIN_DIR)/$@

.PHONY: clean
clean:
	@echo "Limpando os binários executáveis..."
	@rm -rf $(BIN_DIR)
	@echo "Projeto limpo com sucesso!"