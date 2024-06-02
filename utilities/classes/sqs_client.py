"""
SQSClient module

This module contains the SQSClient class which provides methods for interacting with Amazon SQS.

Classes:
    SQSClient: A class for interacting with Amazon SQS.

"""
import json
import boto3
from botocore.exceptions import ClientError
from utilities.settings import LOCALHOST, REGION_NAME

class SQSClient:
    """
    A class for interacting with Amazon SQS.

    Attributes:
        log (CustomLogger): Logger object.
        bucket_name (str): Name of the AWS bucket.
        host (str): Host URL.
        region_name (str): AWS region name.
        mock_aws_flag (bool): Flag indicating whether to mock AWS or not.
        client (boto3.client): SQS client object.
        queue_url (str): URL of the SQS queue.

    Methods:
        __init__: Initializes the SQSClient.
        create_client: Creates an SQS client based on mock_aws_flag.
        create_queue: Creates an SQS queue.
        get_queue_url: Gets the URL of an SQS queue.
        send_message: Sends a message to the SQS queue.
        receive_messages: Receives messages from the SQS queue.
        delete_message: Deletes a message from the SQS queue.
    """

    def __init__(self, log: 'CustomLogger', bucket: str, 
                 mock_aws_flag: bool, host: str = LOCALHOST, region_name: str = REGION_NAME):
        """
        Initialize SQSClient.

        Args:
            log (CustomLogger): Logger object.
            bucket (str): Name of the AWS bucket.
            mock_aws_flag (bool): Flag indicating whether to mock AWS or not.
            host (str, optional): Host URL. Defaults to LOCALHOST.
            region_name (str, optional): AWS region name. Defaults to REGION_NAME.
        """
        self.log = log
        self.bucket_name = bucket
        self.host = host
        self.region_name = region_name
        self.mock_aws_flag = mock_aws_flag
        self.client = self.create_client()
        self.queue_url = ''

    def create_client(self) -> boto3.client:
        """
        Create an SQS client based on mock_aws_flag.

        Returns:
            boto3.client: SQS client object.
        """
        if self.mock_aws_flag:
            return boto3.client(self.bucket_name, 
                                region_name=self.region_name
        )
        
        return boto3.client(self.bucket_name, 
                            endpoint_url=self.host, 
                            region_name=self.region_name
        )

    def create_queue(self, queue_name: str) -> None:
        """
        Create an SQS queue.

        Args:
            queue_name (str): Name of the queue.
        """
        try:
            self.client.create_queue(
                QueueName=queue_name,
                Attributes={
                    "DelaySeconds": "0",
                    "VisibilityTimeout": "60",  # 60 seconds
                }
            )
            self.log.info(f"Queue '{queue_name}' created")
        except ClientError as error:
            self.log.error(error)
            raise error

    def get_queue_url(self, queue_name: str) -> None:
        """
        Get the URL of an SQS queue.

        Args:
            queue_name (str): Name of the queue.
        """
        try:
            response = self.client.get_queue_url(QueueName=queue_name)
            self.log.info(f'URL of queue {queue_name}: {response["QueueUrl"]}')
            self.queue_url = response["QueueUrl"]
        except ClientError as error:
            self.log.error(error)
            raise error

    def send_message(self, car: dict) -> dict:
        """
        Send a message to the SQS queue.

        Args:
            car (dict): Message to be sent.

        Returns:
            dict: Response from the SQS service.
        """
        try:
            message = car
            response = self.client.send_message(QueueUrl=self.queue_url, 
                                                MessageBody=json.dumps(message))
            self.log.info("Message sent")
            return response
        except ClientError as error:
            self.log.error(error)
            raise error

    def receive_messages(self) -> dict:
        """
        Receive messages from the SQS queue.

        Returns:
            dict: Messages received from the SQS service.
        """
        try:
            messages = self.client.receive_message(QueueUrl=self.queue_url, 
                                                   MaxNumberOfMessages=10, 
                                                   WaitTimeSeconds=10)
            self.log.info("Messages received")
            return messages
        except ClientError as error:
            self.log.error(error)
            raise error

    def delete_message(self, receipt_handle: str) -> None:
        """
        Delete a message from the SQS queue.

        Args:
            receipt_handle (str): Receipt handle of the message to be deleted.
        """
        try:
            self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)
            self.log.info("Message deleted")
        except ClientError as error:
            self.log.error(error)
            raise error
