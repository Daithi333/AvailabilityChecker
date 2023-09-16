import os
from pathlib import Path

from controller import Controller

FILE_PATH = os.path.join(Path(__file__).parent, "search_urls.txt")


def handler(event, context):
    controller = Controller(FILE_PATH)
    return controller.process()


if __name__ == '__main__':
    handler({}, None)
