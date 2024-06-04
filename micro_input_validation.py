import zmq


def validate_input_service(input_text):
    valid_characters = "0123456789/. "

    # Check if the input starts with a space or "/"
    if input_text.startswith(" ") or input_text.startswith("/"):
        return {"status": "error", "message": "Input cannot start with a space or '/'."}

    # Count the occurrences of "/", ".", and " "
    slash_count = input_text.count("/")
    comma_count = input_text.count(".")
    space_count = input_text.count(" ")

    # Check for dividing by zero
    if "/" in input_text and input_text.endswith("/0"):
        return {"status": "error", "message": "Cannot divide by zero."}

    # Split the input into whole number and fraction parts
    parts = input_text.split(" ")
    if len(parts) == 2:
        whole_part, fraction_part = parts
        # If there's a "/" in the input, ensure it's at the end (fraction)
        if "/" in whole_part and not "/" in fraction_part:
            return {"status": "error", "message": "Please enter a valid number or fraction."}
    else:
        whole_part = parts[0]
        fraction_part = ""

    # If any of these counts exceed 1, return False
    if slash_count > 1 or comma_count > 1 or space_count > 1 or (slash_count + comma_count > 1) or (comma_count + space_count > 1):
        return {"status": "error", "message": "Exceeded allowed number of special characters. Please enter a valid number or fraction."}

    # Check each character in the input_text
    for char in input_text:
        if char not in valid_characters:
            return {"status": "error", "message": "Please enter a valid number or fraction."}

    return {"status": "success", "message": "Valid input"}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    print("VALIDATION MICROSERVICE HAS STARTED...")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING VALIDATION SERVICE...")
            break
        try:
            input_text = message['input_text']
            result = validate_input_service(input_text)
            response = result
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)


if __name__ == "__main__":
    main()