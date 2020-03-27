
class FileReader:
    
    def __init__(self, filename):
        self.open_file = open(filename)
        self.urls = self._read_lines()
        self._close()

    def _read_lines(self):
        lines = []
        for line in self.open_file:
            lines.append(line)
        return lines

    def _close(self):
        self.open_file.close()
