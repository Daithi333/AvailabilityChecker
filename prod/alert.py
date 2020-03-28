import boto3

from config import config


class Alert:

    def __init__(self):
        self.sns = boto3.client('sns')

    def send(self, message):
        arn = config['TopicArn']
        return self.sns.publish(TopicArn=arn, Message=message)
