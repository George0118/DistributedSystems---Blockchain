import json

def process_command(string):
    splits = string.split(" ")
    command_info = {}

    if splits[0] != "transaction":
        print(f"Unknown command {splits[0]}.")
    else:
        command_info["receiver"] = int(splits[1])
        command_info["type"] = splits[2]

        if command_info["type"] == "message":
            command_info["type"] == "Exchange"
            command_info["data"] = splits[3]
        elif command_info["type"] == "amount":
            command_info["type"] == "Exchange"
            command_info["amount"] = int(splits[3])
        elif command_info["type"] == "stake":
            command_info["type"] == "Stake"
            command_info["amount"] = int(splits[3])
        elif command_info["type"] == "initialization":
            command_info["type"] == "Initialization"
            command_info["amount"] = int(splits[3])
        else:
            print(f"Unknown transaction type {splits[2]}.")

    return json.dumps(command_info)

        
        
