import json
import os


def load_messages(queue_file: str):
    if not os.path.exists(queue_file):
        return []

    with open(queue_file, "r") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_messages(queue_file: str, messages: list):
    with open(queue_file, "w") as f:
        json.dump(messages, f, indent=2)


def get_next_message(queue_file: str):
    messages = load_messages(queue_file)

    if not messages:
        return None

    next_message = messages.pop(0)
    save_messages(queue_file, messages)
    return next_message


def push_message(queue_file: str, message: dict):
    messages = load_messages(queue_file)
    messages.append(message)
    save_messages(queue_file, messages)