# Testing AWS Services With Python

[![Pylint](https://github.com/Jmateusribeiro/Testing_AWS_Services_Python/actions/workflows/pylint.yml/badge.svg)](https://github.com/Jmateusribeiro/Testing_AWS_Services_Python/actions/workflows/pylint.yml)

## Overview
This project serves as a starter guide to testing AWS services with Python. It presents a methodology for testing AWS infrastructure and explores two approaches: leveraging LocalStack and utilizing Moto for mocking.

### LocalStack
LocalStack provides a fully functional local AWS cloud stack, allowing developers to test AWS services locally without affecting the live AWS environment. By utilizing LocalStack, developers can simulate AWS services locally, facilitating integration testing in a controlled environment.

### Moto
Moto is a library that allows developers to mock AWS services for testing purposes. It provides a lightweight solution for simulating AWS services in unit tests, offering flexibility and simplicity in setting up mock environments.

## Choosing Between LocalStack and Moto
The choice between LocalStack and Moto depends on the specific testing requirements and preferences of the project. 
- **LocalStack** is ideal for integration testing, as it closely replicates the behavior of AWS services in a local environment. It is suitable for end-to-end testing scenarios where interactions between multiple AWS services are involved.
- **Moto**, on the other hand, is more lightweight and is primarily used for unit testing. It is suitable for testing individual components or functionalities in isolation, without the need for a full integration environment.

It is possible to select the desired testing approach using a command-line option (`--mock-aws`) when running the tests. By default, Moto is used for mocking AWS services. However, if one prefer to use LocalStack for local testing, use command line option `--mock-aws=False`. 

## Dependencies
Before running the tests, ensure you have the following dependencies installed:
- **Python:** Make sure you have Python installed on your system.

- **Docker:** LocalStack requires Docker to run. Install Docker Desktop if you haven't already: [Docker Desktop](https://www.docker.com/products/docker-desktop)

- **AWS CLI:** Install the AWS Command Line Interface (CLI) to configure AWS credentials and interact with AWS services locally. You can install the AWS CLI using pip:

  ```bash
  pip install awscli
- **Python packages:** listed in `requirements.txt`


## AWS Services Tested
- **SQS:** Tests cover functionality related to cars stream processing.

### TODO:
- Explore additional SQS functionalities and test cases.
- Testing other AWS services such as S3.

## Testing Approach
Tests are implemented using the Behavior-Driven Development (BDD) style, offering a clear and understandable structure for defining test scenarios.

## Running Tests
Execute the `run_tests.bat` batch file to run all tests. Each execution generates a comprehensive HTML report stored in the `reports` folder.

**Note:** Make sure to run the batch file within an environment with all necessary dependencies installed.

---

Enjoy exploring and testing AWS services with Python! If you have any questions or feedback, feel free to reach out.
