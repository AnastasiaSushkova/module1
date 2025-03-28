import os

def read_file_lines(filename):
    if not os.path.exists(filename):
        print(f"Файл не знайдено: {filename}")
        return set()
    with open(filename, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file if line.strip())
