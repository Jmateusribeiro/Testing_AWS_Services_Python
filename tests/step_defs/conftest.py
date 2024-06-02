"""
conftest module
"""
from moto import mock_aws
import pytest
from utilities.classes.sqs_client import SQSClient
from utilities.classes.log import CustomLogger
from utilities.settings import QUEUE_NAME, SQS_BUCKET, REPORT_DIR
from utilities import os_funcs as cmd

def pytest_addoption(parser: 'pytest.Parser') -> None:
    """
    Add custom command-line option for pytest.

    Args:
        parser (pytest.Parser): The pytest parser object.
    """
    parser.addoption("--mock-aws",
                     action="store",
                     default="True",
                     choices=["True", "False"],
                     type=str,
                     help="Boolean to indicate if AWS should be mocked"
    )

@pytest.fixture(scope='module')
def mock_aws_flag(request: 'pytest.FixtureRequest') -> bool:
    """
    Fixture to retrieve the value of the --mock-aws option.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object.

    Returns:
        bool: Boolean indicating whether AWS should be mocked.
    """
    mock_aws_value = request.config.getoption("--mock-aws")
    mock_aws_flag_value = mock_aws_value == "True"

    return mock_aws_flag_value

@pytest.fixture(scope='module')
def log() -> CustomLogger:
    """
    Fixture to create a CustomLogger instance.

    Returns:
        CustomLogger: A CustomLogger instance.
    """
    return CustomLogger(REPORT_DIR)

@pytest.fixture(autouse=True, scope='module')
def setup(request: 'pytest.FixtureRequest', mock_aws_flag: bool, log: CustomLogger) -> None:
    """
    Fixture to setup AWS mocking or LocalStack based on the mock_aws_flag.

    Args:
        request (pytest.FixtureRequest): The pytest fixture request object.
        mock_aws_flag (bool): Boolean indicating whether AWS should be mocked.
        log (CustomLogger): A CustomLogger instance.
    """
    log.info(f"AWS Mock Flag: {mock_aws_flag}")

    if mock_aws_flag:
        # Setup mocked AWS environment
        log.info("Creating mocked SQS client")
        mock = mock_aws()
        mock.start()

        def teardown():
            # Teardown mocked AWS environment
            mock.stop()

        request.addfinalizer(teardown)
    else:
        # Setup LocalStack environment
        log.info("Creating real SQS client")
        log.info("\nStart LocalStack\n")
        cmd.start_localstack()

        def teardown():
            # Teardown LocalStack environment
            log.info("\nStop LocalStack")
            cmd.stop_localstack()

        request.addfinalizer(teardown)

@pytest.fixture()
def sqs_cli(mock_aws_flag: bool, log: CustomLogger) -> SQSClient:
    """
    Fixture to create an SQSClient instance.

    Args:
        mock_aws_flag (bool): Boolean indicating whether AWS should be mocked.
        log (CustomLogger): A CustomLogger instance.

    Returns:
        SQSClient: An SQSClient instance.
    """
    sqs_client_instance = SQSClient(log=log, bucket=SQS_BUCKET, mock_aws_flag=mock_aws_flag)
    sqs_client_instance.create_queue(QUEUE_NAME)
    sqs_client_instance.get_queue_url(QUEUE_NAME)

    return sqs_client_instance
