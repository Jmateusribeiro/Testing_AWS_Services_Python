"""
This module contains all the settings required
"""
import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
queue_name = "cars"
host = "http://localhost:4566"
sqs_bucket = "sqs"
