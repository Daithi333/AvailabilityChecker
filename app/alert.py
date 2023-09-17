import boto3


class Alert:

    def __init__(self):
        self.sns = boto3.client('sns')

    def send(self, topic_arn: str, message: str):
        return self.sns.publish(TopicArn=topic_arn, Message=message)
