import zmq


def convertor(value, input_unit, output_unit):
    conversions = {
        'tsp': {'tsp': 1, 'tbsp': 1/3, 'cups': 1/48},
        'tbsp': {'tsp': 3, 'tbsp': 1, 'cups': 1/16},
        'cups': {'tsp': 48, 'tbsp': 16, 'cups': 1}
    }

    if input_unit not in conversions or output_unit not in conversions[input_unit]:
        raise ValueError(f"Unsupported units: {input_unit} to {output_unit}")

    converted_value = round(value * conversions[input_unit][output_unit], 2)
    return converted_value


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("CONVERSION MICROSERVICE HAS STARTED...")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING CONVERSION SERVICE...")
            break
        try:
            value = message['value']
            input_unit = message['input_unit']
            output_unit = message['output_unit']
            result = convertor(value, input_unit, output_unit)
            response = {"status": "success", "data": result}
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)


if __name__ == "__main__":
    main()