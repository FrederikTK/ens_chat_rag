#this script generates a unique id for each run of the program
import uuid
import os

def generate_unique_id(log_path):
    existing_ids = set()
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            # Read the entire file content and split by spaces to handle UUIDs on the same line
            existing_ids = set(file.read().split())

    while True:
        new_id = str(uuid.uuid4())
        if new_id not in existing_ids:
            with open(log_path, 'a') as file:
                # Add the new UUID followed by a space to maintain the current formatting
                file.write(new_id + ' ')
            return new_id