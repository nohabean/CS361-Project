import socket


def tcp_server():
    """
        Runs a TCP server that listens for incoming connections on localhost (127.0.0.1)
        and a specified port (54321). The server accepts connections from clients and
        communicates with them, echoing back any received messages until the client sends
        the message 'exit' to terminate the connection and shut down the server.

        Returns:
            None
    """

    # Create a Socket:
    # socket(): Create a TCP/IP socket using AF_INET for IPv4 and SOCK_STREAM for TCP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the Socket:
    # bind(): Bind the socket to a specific IP address and port
    server_address = '127.0.0.1'
    server_port = 54321
    server_sock.bind((server_address, server_port))

    # Listen for Incoming Connections:
    # listen(): Put the socket into server mode and listen for incoming connections
    server_sock.listen(5)

    print("Server is listening for incoming connections...")

    try:
        # Main server loop while the server is running
        while True:
            # Accept Connections:
            # accept(): Accept a new connection
            client_sock, client_address = server_sock.accept()
            print(f"Connection from {client_address}")

            try:
                # Send and Receive Data:
                # recv(): Receive data from the client
                message = client_sock.recv(1024).decode()
                print(f"Received message from {client_address}: {message}")

                # sendall(): Send a response back to the client
                response = f"Message received: {message}"
                client_sock.sendall(response.encode())
                print("Response sent to client")

            finally:
                # Close Client Connection:
                # close() (on the client socket): Close the client connection
                client_sock.close()
                print(f"Connection with {client_address} closed")

    except KeyboardInterrupt:
        print("Server is shutting down")

    finally:
        # Close Server Socket:
        # close() (on the server socket): Close the server socket
        server_sock.close()
        print("Server socket closed")


if __name__ == "__main__":
    tcp_server()
