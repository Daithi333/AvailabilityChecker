
class FileReader:
    
    def __init__(self, filename):
        self.filename = filename

    def read_lines(self):
        lines = []
        open_file = open(self.filename)
        for line in open_file:
            lines.append(line)
        open_file.close()
        print('%s urls read from file' % len(lines))
        return lines
