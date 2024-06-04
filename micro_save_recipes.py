import zmq

def save_recipe_calculations_service(data, file_path):
    try:
        with open(file_path, "w") as file:
            for entry in data:
                item_name = entry.get('item_name', '')
                measurement_value = entry.get('measurement_value', '')
                measurement_unit = entry.get('measurement_unit', '')
                operation = entry.get('operation', '')
                calc_factor = entry.get('calc_factor', '')
                calc_result_value = entry.get('calc_result_value', '')
                file.write(f"Item Name: {item_name}\n")
                file.write(f"Measurement: {measurement_value} {measurement_unit}\n")
                file.write(f"Operation: {operation} {calc_factor}\n")
                file.write(f"Result: {calc_result_value}\n\n")
        return {"status": "success", "message": f"Data saved to {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")  # Choose a port for the microservice
    print("SAVE RECIPE CALCULATIONS MICROSERVICE HAS STARTED...")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING SAVE SERVICE...")
            break
        try:
            data = message['data']
            file_path = message['file_path']
            result = save_recipe_calculations_service(data, file_path)
            response = result
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)

if __name__ == "__main__":
    main()