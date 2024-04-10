import json

def read_input(queue, stop_event, id):
    while not stop_event.is_set():
        user_input = input(f"> {id.upper()}").strip()
        if user_input.lower() == "exit":
            stop_event.set()  # Set the stop event to signal threads to exit
            break
        elif user_input:
            try:
                queue.put(user_input.strip())  # Put the command into the appropriate thread's queue
            except ValueError:
                print("Invalid input format. Please enter in the format 'idN: command'.")

def process_command(string):
    splits = string.split(" ", 2)
    command_info = {}

    if splits[0] == "t":
        command_info["receiver"] = splits[1]
        command_info["type"] = "Exchange"
        command_info["amount"] = int(splits[2])

    elif splits[0] == "m":
        command_info["receiver"] = splits[1]
        command_info["type"] = "Exchange"
        command_info["message"] = splits[2]

    elif splits[0] == "stake":
        command_info["receiver"] = 0
        command_info["type"] = "Stake"
        command_info["amount"] = int(splits[1])

    else:
        print(f"\nUnknown command {splits[0]}")
        return None

    return json.dumps(command_info)        