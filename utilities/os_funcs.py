import os


def start_localstack():

    os.system("start cmd /c localstack start")


def stop_localstack():
    os.system('localstack stop')
