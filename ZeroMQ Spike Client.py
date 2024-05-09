#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:1234")

print(f"Sending request to the server…")
socket.send(b"A message from CS361")

print(f"Sent: A message from CS361")

#  Get the reply.
message = socket.recv()
print(f"Received reply: {message}")
