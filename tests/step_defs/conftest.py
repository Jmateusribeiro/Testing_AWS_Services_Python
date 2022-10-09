import pytest
from utilities.classes.sqs_client import SQSClient
from utilities.settings import queue_name, host, sqs_bucket
from utilities import os_funcs as cmd


@pytest.fixture(autouse=True, scope='module')
def setup(request):

    # Setup code
    print("\nStart LocalStack\n")
    cmd.start_localstack()

    def teardown():
        # Teardown code
        print("\nStop LocalStack")
        cmd.stop_localstack()

    request.addfinalizer(teardown)


@pytest.fixture()
def sqs_cli():

    sqs_cli = SQSClient(bucket=sqs_bucket, host=host)
    sqs_cli.create_queue(queue_name)
    sqs_cli.get_queue_url(queue_name)

    return sqs_cli
