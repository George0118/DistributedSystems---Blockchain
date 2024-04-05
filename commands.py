import json

def process_command(string):
    splits = string.split(" ")
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
        command_info["receiver"] = splits[1]
        command_info["type"] = "Stake"
        command_info["amount"] = int(splits[2])

    else:
        print(f"\nUnknown command {splits[0]}")
        return None

    return json.dumps(command_info)

        
        
