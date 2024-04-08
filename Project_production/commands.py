import json        
from queue import Queue
from config import N

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


def file_parsing(id):
    file_name = "trans" + id[2] + ".txt"
    folder_name = "input_" + str(N)
    file_path = folder_name + "/" + file_name
    queue = Queue()

    with open(file_path, 'r') as file:
        for line in file:
            command = "m " + line.strip()
            queue.put(command)
    return queue