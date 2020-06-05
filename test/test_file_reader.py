from unittest.mock import patch, mock_open

from app.file_reader import FileReader


def test_builtin_open_called_with_filename():
    with patch('builtins.open', mock_open()) as m:
        file_reader = FileReader('filename')
        file_reader.read_lines()
        m.assert_called_with('filename')


def test_file_reader_returns_list_of_lines():
    with patch('builtins.open', mock_open(read_data='line 1\nline 2\nline 3')):
        file_reader = FileReader('filename')
        result = file_reader.read_lines()
        assert result[0] == 'line 1\n'
        assert len(result) == 3
