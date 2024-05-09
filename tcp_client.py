import socket


def tcp_client():
    """
        Runs a TCP client that connects to a server running on localhost (127.0.0.1)
        and a specified port (54321). The client sends messages to the server and
        receives responses. It continues to send messages until the user inputs 'exit',
        which terminates the connection and closes the client.

        Returns:
            None
    """


    # Create a Socket:
    # socket(): Create a TCP/IP socket using AF_INET for IPv4 and SOCK_STREAM for TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Specify Server Address and Port:
    # Define the server's IP address and port number to connect to
    server_address = '127.0.0.1'
    server_port = 54321

    try:
        # Establish a Connection:
        # connect(): Connect the socket to the server's address and port
        sock.connect((server_address, server_port))
        print("Connected to the server.")

        # While the user has not entered the specific input
        while True:
            # Send and Receive Data:
            # Prompt user for input to send the exit message to the server
            # sendall(): Send data to the server
            message = "A message from CS361"
            sock.sendall(message.encode())

            print("Message sent to server")

            # recv(): Receive data from the server, specifying the buffer size
            response = sock.recv(1024).decode()
            if not response:            # if response is empty, close the connection
                print("Server close the connection")
                break
            print(f"Received response: {response}")

    finally:
        # Close the Connection:
        # close(): Close the socket to free up resources
        sock.close()


if __name__ == "__main__":
    tcp_client()
