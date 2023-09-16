
class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_lines(self):
        with open(self.filename, "r") as file:
            lines = [line.strip() for line in file]

        print('%s urls read from file' % len(lines))
        return lines
