"""
steps to scenarios of cars_stream_processing feature
"""
import json
from pytest_bdd import scenarios, given, when, then
from utilities.settings import PROJECT_DIR

# Load feature files for pytest-bdd
scenarios('../features/cars_stream_processing.feature')

# Given Step
@given('a list of cars are added to car queue', target_fixture='cars_list')
def added_cars(sqs_cli: 'SQSClient', log: 'CustomLogger') -> list:
    """
    Given step to add a list of cars to the car queue.

    Args:
        sqs_cli (SQSClient): An instance of SQSClient.
        log (CustomLogger): A CustomLogger instance.

    Returns:
        list: List of cars added to the queue.
    """
    log.info("########   Start Step: 'Given a list of cars are added to car queue'   ########")
    #f = open(PROJECT_DIR + "\\test-data\\cars.json", "r")
    #cars = json.loads(f.read())
    with open(PROJECT_DIR + "\\test-data\\cars.json", "r", encoding='utf-8') as f:
        cars = json.loads(f.read())

    for car in cars:
        car_details = car["car detail"]

        resp = sqs_cli.send_message(car_details)

        car["id"] = resp["MessageId"]

        log.info(f"car details: {car}")

    log.info("########   End Step: 'Given a list of cars are added to car queue'   ########")

    return cars

# When Step
@when("the queue list is returned", target_fixture='messages')
def queue_list(sqs_cli: 'SQSClient', log: 'CustomLogger') -> dict:
    """
    When step to return the queue list.

    Args:
        sqs_cli (SQSClient): An instance of SQSClient.
        log (CustomLogger): A CustomLogger instance.

    Returns:
        dict: Queue list.
    """
    log.info("########   Start Step: 'When the queue list is returned'   ########")

    messages = sqs_cli.receive_messages()

    log.info("########   End Step: 'When the queue list is returned'   ########")

    return messages

# Then Step
@then("the list contains the cars added")
def assert_response_code(sqs_cli: 'SQSClient', 
                         cars_list: list, messages: dict, log: 'CustomLogger') -> None:
    """
    Then step to assert that the list contains the cars added.

    Args:
        sqs_cli (SQSClient): An instance of SQSClient.
        cars_list (list): List of cars added to the queue.
        messages (dict): Queue list.
        log (CustomLogger): A CustomLogger instance.
    """
    log.info("########   Start Step: 'Then the list contains the cars added'   ########")
    messages_count = 0
    for message in messages["Messages"]:
        in_message_id = message["MessageId"]
        body = message["Body"]
        receipt_handle = message["ReceiptHandle"]

        log.info(f"message body: {message}")

        for car in cars_list:

            car_details = car["car detail"]
            out_message_id = car["id"]

            if in_message_id == out_message_id:
                error_msg = f"body of the message {in_message_id} doesn't match car detail"
                assert car_details == json.loads(body), error_msg

                log.info(f"delete message with id {in_message_id}")
                sqs_cli.delete_message(receipt_handle)
                messages_count += 1
    
    error_messages = f"""Couldn't find all messages sent. 
    Were sent {len(cars_list)} msgs, 
    but found only {messages_count} msgs"""
    assert len(cars_list) == messages_count, error_messages

    log.info("########   End Step: 'Then the list contains the cars added'   ########")
