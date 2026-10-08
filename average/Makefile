TARGET = average
SRC = main.asm
OBJ = main.o

all: $(TARGET)

$(TARGET): $(OBJ)
	ld $(OBJ) -o $(TARGET)

$(OBJ): $(SRC)
	nasm -f elf64 $(SRC) -o $(OBJ)

run: $(TARGET)
	./$(TARGET) data.txt

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all run clean
