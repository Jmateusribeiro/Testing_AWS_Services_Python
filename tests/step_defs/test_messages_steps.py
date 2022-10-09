from pytest_bdd import scenarios, given, when, then
import json
import pytest
from utilities.settings import project_dir


scenarios('../features/cars_stream_processing.feature')


# Given Step
@given('a list of cars are added to car queue', target_fixture='added_cars')
def added_cars(sqs_cli):

    print("\nStart Step: 'a list of cars are added to car queue':\n")
    f = open(project_dir+"\\test-data\\cars.json", "r")
    cars = json.loads(f.read())

    for car in cars:
        car_details = car["car detail"]

        resp = sqs_cli.send_message(car_details)

        car["id"] = resp["MessageId"]

        print(f"car details: {car}")

    print("\nEnd Step: 'a list of cars are added to car queue':\n")

    return cars


# When Step
@when("the queue list is returned", target_fixture='queue_list')
def queue_list(sqs_cli):

    print("\nStart Step: 'the queue list is returned':\n")

    messages = sqs_cli.receive_messages()

    print("\nStop Step: 'the queue list is returned':\n")

    return messages


# Then Steps
@then("the list contains the cars added")
def assert_response_code(sqs_cli, added_cars, queue_list):

    print("\nStart Step: 'the list contains the cars added':\n")
    messages_count = 0
    for message in queue_list["Messages"]:
        in_message_id = message["MessageId"]
        body = message["Body"]
        receipt_handle = message["ReceiptHandle"]

        print(f"message body: {message}")

        for car in added_cars:

            car_details = car["car detail"]
            out_message_id = car["id"]

            if in_message_id == out_message_id:

                assert car_details == json.loads(body), f"body of the message {in_message_id} doesn't match car detail"

                print(f"delete message with id {in_message_id}")
                sqs_cli.delete_message(receipt_handle)
                messages_count = messages_count + 1


    assert len(added_cars) == messages_count, f"Couldn't find all messages sent. Were sent {len(added_cars)} msgs, but found only {messages_count} msgs"

    print("\nStop Step: 'the list contains the cars added':\n")
