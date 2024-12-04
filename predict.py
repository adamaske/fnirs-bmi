import numpy as np
import time
import socket
import struct
from pylsl import StreamInlet
from pylsl import resolve_stream

import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from keras.utils import to_categorical


# Server
server_host = '192.168.50.53'  # Localhost
server_port = 65432 # port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen()#  Start listening for incoming connections
print(f"Server listening on {server_host}:{server_port}...")
client_socket, client_address = server_socket.accept() # Accept a connection from a client
print(f"Connection established with {client_address}")

# LSL Inlet
inlet = StreamInlet(resolve_stream('type', 'fNIRS')[0])


#load model
model_path = "models/model_01"
model = load_model(model_path)

channel_count = 102
sampling_frequency = 5.1
recording = True
while recording:
    data = inlet.pull_sample()
    
# read data

# preprocess data


# segment data


# model.predict()

# prediction 
chosen_label = 0

try:
    while True:
        # Prepare an array of floats to send
        thetas = np.random.random(6)
        #Convert the float array to bytes using struct (format 'f' for float)
        byte_data = struct.pack(f"<6f", *thetas)
        #Send the byte data to the client
        client_socket.sendall(byte_data)
        print(f"Sent floats: {thetas}")

        x = input()
except(KeyboardInterrupt):
    client_socket.close()
    server_socket.close()