from prod.controller import Controller


def handler(event, context):
    print(str(event))
    controller = Controller()
    return controller.process()
