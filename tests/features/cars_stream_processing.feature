Feature: Cars Stream Processing

  the cars added to the queue are defined in the file 'test-data\cars.json'

  Scenario: Messages are consumed successfully
    Given a list of cars are added to car queue
    When the queue list is returned
    Then the list contains the cars added