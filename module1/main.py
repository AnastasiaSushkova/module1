import os

def read_file_lines(filename):
    if not os.path.exists(filename):
        print(f"Файл не знайдено: {filename}")
        return set()
    with open(filename, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file if line.strip())

def write_lines_to_file(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        for line in sorted(lines):
            file.write(line + '\n')

def compare_files(file1, file2, same_output="same.txt", diff_output="diff.txt"):
    lines1 = read_file_lines(file1)
    lines2 = read_file_lines(file2)

    same_lines = lines1 & lines2
    diff_lines = lines1 ^ lines2

    write_lines_to_file(same_output, same_lines)
    write_lines_to_file(diff_output, diff_lines)

    print(f"Спільні рядки збережено в '{same_output}'")
    print(f"Відмінні рядки збережено в '{diff_output}'")
    print(f"Спільних рядків: {len(same_lines)}, Відмінних: {len(diff_lines)}")
