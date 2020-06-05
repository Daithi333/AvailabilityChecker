from app.controller import Controller


def handler(event, context):
    controller = Controller()
    return controller.process()
