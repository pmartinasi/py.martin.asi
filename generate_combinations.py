@ -1,32 +0,0 @@
import itertools
import string
import sys

def generate_combinations(min_length, max_length):
    all_chars = string.printable[:-5]  # Obtener todos los caracteres ASCII imprimibles excepto los últimos cinco (\n, \r, \x0b, \x0c, \x0d)
    for length in range(min_length, max_length + 1):
        for combination in itertools.product(all_chars, repeat=length):
            yield ''.join(combination)

def save_to_file(filename, min_length, max_length):
    for result in generate_combinations(min_length, max_length):
        f = open(filename, "a")
        f.write(result + '\n')
        f.close()
        print(result)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python generate_combinations.py min_length max_length output_file.txt")
        sys.exit(1)

    min_length = int(sys.argv[1])
    max_length = int(sys.argv[2])
    output_file = sys.argv[3]

    if min_length < 1 or max_length < min_length:
        print("Los argumentos deben ser positivos y max_length debe ser mayor o igual que min_length.")
        sys.exit(1)

    save_to_file(output_file, min_length, max_length)
    print(f"Combinaciones generadas y guardadas en '{output_file}'.")