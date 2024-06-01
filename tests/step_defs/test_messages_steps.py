from pytest_bdd import scenarios, given, when, then
import json
from utilities.settings import project_dir

# Load feature files for pytest-bdd
scenarios('../features/cars_stream_processing.feature')

# Given Step
@given('a list of cars are added to car queue', target_fixture='added_cars')
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
    f = open(project_dir + "\\test-data\\cars.json", "r")
    cars = json.loads(f.read())

    for car in cars:
        car_details = car["car detail"]

        resp = sqs_cli.send_message(car_details)

        car["id"] = resp["MessageId"]

        log.info(f"car details: {car}")

    log.info("########   End Step: 'Given a list of cars are added to car queue'   ########")

    return cars

# When Step
@when("the queue list is returned", target_fixture='queue_list')
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
def assert_response_code(sqs_cli: 'SQSClient', added_cars: list, queue_list: dict, log: 'CustomLogger') -> None:
    """
    Then step to assert that the list contains the cars added.

    Args:
        sqs_cli (SQSClient): An instance of SQSClient.
        added_cars (list): List of cars added to the queue.
        queue_list (dict): Queue list.
        log (CustomLogger): A CustomLogger instance.
    """
    log.info("########   Start Step: 'Then the list contains the cars added'   ########")
    messages_count = 0
    for message in queue_list["Messages"]:
        in_message_id = message["MessageId"]
        body = message["Body"]
        receipt_handle = message["ReceiptHandle"]

        log.info(f"message body: {message}")

        for car in added_cars:

            car_details = car["car detail"]
            out_message_id = car["id"]

            if in_message_id == out_message_id:

                assert car_details == json.loads(body), f"body of the message {in_message_id} doesn't match car detail"

                log.info(f"delete message with id {in_message_id}")
                sqs_cli.delete_message(receipt_handle)
                messages_count += 1

    assert len(added_cars) == messages_count, f"Couldn't find all messages sent. Were sent {len(added_cars)} msgs, but found only {messages_count} msgs"

    log.info("########   End Step: 'Then the list contains the cars added'   ########")
