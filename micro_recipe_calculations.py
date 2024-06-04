import zmq


def calculate_recipe(measurement_value, operation, calc_factor):
    if operation == "Multiply":
        return round(measurement_value * calc_factor, 2)
    elif operation == "Divide":
        return round(measurement_value / calc_factor, 2)
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("RECIPE CALCULATION MICROSERVICE HAS STARTED...")

    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING RECIPE CALCULATION SERVICE...")
            break

        try:
            measurement_value = message['measurement_value']
            operation = message['operation']
            calc_factor = message['calc_factor']
            result = calculate_recipe(measurement_value, operation, calc_factor)

            response = {"status": "success", "data": result}
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)


if __name__ == "__main__":
    main()