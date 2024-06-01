import os

def start_localstack() -> None:
    """
    Start local stack on command line.
    """
    os.system("start cmd /c localstack start")


def stop_localstack() -> None:
    """
    Stop local stack on command line.
    """
    os.system('localstack stop')
