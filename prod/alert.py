import boto3


class Alert:

    def __init__(self):
        self.sns = boto3.client('sns')
        self.arn = "arn:aws:sns:eu-west-1:757607970807:ProductAlert"

    def send(self, message):
        self.sns.publish(TopicArn=self.arn, Message=message)