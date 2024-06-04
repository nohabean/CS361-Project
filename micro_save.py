import zmq
import os

def save_conversions_service(data, file_path):
    try:
        with open(file_path, "w") as file:
            for entry in data:
                file.write(f"{entry['input']} {entry['input_unit']} = {entry['output']} {entry['output_unit']}\n")
        return {"status": "success", "message": f"Data saved to {file_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")
    print("SAVE CONVERSIONS MICROSERVICE HAS STARTED...")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING SAVE SERVICE...")
            break
        try:
            data = message['data']
            file_path = message['file_path']
            result = save_conversions_service(data, file_path)
            response = result
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)

if __name__ == "__main__":
    main()