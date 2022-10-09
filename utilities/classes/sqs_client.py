import boto3
from botocore.exceptions import ClientError
import json


class SQSClient:
    def __init__(self, bucket, host):
        self.name = bucket
        self.host = host
        self.client = boto3.client(bucket, endpoint_url=host)
        self.queue_url = ''

    def create_queue(self, queue_name):

        try:
            self.client.create_queue(
                QueueName=queue_name,
                Attributes={
                    "DelaySeconds": "0",
                    "VisibilityTimeout": "60",  # 60 seconds
                }
            )

            print(f"queue '{queue_name}' created")

        except ClientError as error:
            raise error

    def get_queue_url(self, queue_name):

        try:
            response = self.client.get_queue_url(
                QueueName=queue_name,
            )

            print(f'url of queue {queue_name}: {response["QueueUrl"]}')

            self.queue_url = response["QueueUrl"]

        except ClientError as error:
            raise error

    def send_message(self, car):

        try:

            message = car
            response = self.client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message)
            )

            print(f"message sent")
            return response

        except ClientError as error:
            raise error

    def receive_messages(self):

        try:
            messages = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
            )

            print(f"messages received")
            return messages

        except ClientError as error:
            raise error

    def delete_message(self, receipt_handle):

        try:
            self.client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle,
            )

            print(f"message deleted")

        except ClientError as error:
            raise error