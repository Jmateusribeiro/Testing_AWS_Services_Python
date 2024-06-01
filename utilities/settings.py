import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
report_dir  = project_dir + "//reports"
queue_name  = "cars"
localhost   = "http://localhost:4566"
sqs_bucket  = "sqs"
region_name = "eu-west-2"
