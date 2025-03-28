import pytest
from main import read_file_lines, write_lines_to_file, compare_files


@pytest.fixture
def temp_files(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    same = tmp_path / "same.txt"
    diff = tmp_path / "diff.txt"
    return file1, file2, same, diff


def test_read_file_lines(tmp_path):
    file = tmp_path / "input.txt"
    file.write_text("apple\nbanana\napple\n  cherry  \n\n")
    result = read_file_lines(file)
    assert result == {"apple", "banana", "cherry"}


def test_write_lines_to_file(tmp_path):
    file = tmp_path / "output.txt"
    lines = {"banana", "apple", "cherry"}
    write_lines_to_file(file, lines)
    content = file.read_text().splitlines()
    assert content == sorted(lines)


@pytest.mark.parametrize("content1, content2, expected_same, expected_diff", [
    (
        {"apple", "banana", "cherry"},
        {"banana", "cherry", "date"},
        {"banana", "cherry"},
        {"apple", "date"}
    ),
    (
        {"one", "two"},
        {"three", "four"},
        set(),
        {"one", "two", "three", "four"}
    ),
])
def test_compare_files(temp_files, content1, content2, expected_same, expected_diff):
    file1, file2, same_path, diff_path = temp_files

    write_lines_to_file(file1, content1)
    write_lines_to_file(file2, content2)

    compare_files(file1, file2, same_output=same_path, diff_output=diff_path)

    same_result = read_file_lines(same_path)
    diff_result = read_file_lines(diff_path)

    assert same_result == expected_same, f"Expected same: {expected_same}, got: {same_result}"
    assert diff_result == expected_diff, f"Expected diff: {expected_diff}, got: {diff_result}"


def test_identical_files(temp_files):
    file1, file2, same, diff = temp_files
    lines = {"a", "b", "c"}
    write_lines_to_file(file1, lines)
    write_lines_to_file(file2, lines)

    compare_files(file1, file2, same_output=same, diff_output=diff)

    assert read_file_lines(same) == lines
    assert read_file_lines(diff) == set()

def test_completely_different_files(temp_files):
    file1, file2, same, diff = temp_files
    write_lines_to_file(file1, {"a", "b"})
    write_lines_to_file(file2, {"x", "y"})

    compare_files(file1, file2, same_output=same, diff_output=diff)

    assert read_file_lines(same) == set()
    assert read_file_lines(diff) == {"a", "b", "x", "y"}

def test_empty_files(temp_files):
    file1, file2, same, diff = temp_files
    file1.write_text("")
    file2.write_text("")

    compare_files(file1, file2, same_output=same, diff_output=diff)

    assert read_file_lines(same) == set()
    assert read_file_lines(diff) == set()

def test_whitespace_and_newlines(temp_files):
    file1, file2, same, diff = temp_files
    file1.write_text("line1 \n line2\n")
    file2.write_text("line1\nline3\n")

    compare_files(file1, file2, same_output=same, diff_output=diff)

    assert read_file_lines(same) == {"line1"}
    assert read_file_lines(diff) == {"line2", "line3"}
