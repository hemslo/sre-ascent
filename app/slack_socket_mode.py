#!/usr/bin/env python3

from app import config
from app.dependencies.slack_handler import slack_socket_model_handler


def run():
    if config.SLACK_APP_TOKEN:
        slack_socket_model_handler.start()
    else:
        print("SLACK_APP_TOKEN not found.")


if __name__ == '__main__':
    run()
