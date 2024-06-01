import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
REPORT_DIR  = PROJECT_DIR + "//reports"
QUEUE_NAME  = "cars"
LOCALHOST   = "http://localhost:4566"
SQS_BUCKET  = "sqs"
REGION_NAME = "eu-west-2"
