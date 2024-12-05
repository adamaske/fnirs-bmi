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

from inverse_kinematics import ik

# Server
server_host = '192.168.50.53'  # Localhost
server_port = 65432 # port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen()#  Start listening for incoming connections
print(f"Server listening on {server_host}:{server_port}...")
client_socket, client_address = server_socket.accept() # Accept a connection from a client
print(f"Connection established with {client_address}")

inlet = StreamInlet(resolve_stream('type', 'fNIRS')[0]) #connect to LSL stream


#load model
model_path = "models/model_good"
model = load_model(model_path)

channels = 102
sampling_frequency = 5.1
timesteps = 50
recording = True

classes = ["rest", "right", "left"]

home_position = np.array(((1, 2, 3))) # UR5e end-effector position at the home configuration
desired_position = home_position
def move_desired_position(direction):
    
    if direction == "right":
        desired_position += np.array(((0, 0, 0)))
    if direction == "left":
        desired_position += np.array(((0, 0, 0)))
        
    return desired_position

def send_desired_joing_angles(position):
    thetas = ik(position) # calculate IK 
    byte_data = struct.pack(f"<{len(thetas)}f", *thetas)
    client_socket.sendall(byte_data)
    print(f"predict -> Sent desired joint angles : {thetas}")

def realtime_control():
    while recording:
        sample_count = 0
        sample = []

        while sample_count < timesteps:
            data =  inlet.pull_sample()
            sample.append(data)
            sample_count += 1
            
        sample = np.array(sample)

        #preprocess data
        #Turn to hemoglobin
        #hb = np.array(hb)
        #
        sample.reshape(-1, channels, timesteps)

        prediction = model.predict(sample)
        prediction_class = np.argmax(prediction, axis=1)

        new_position = move_desired_position(classes[prediction_class])
        send_desired_joing_angles(desired_position)

try:  
    realtime_control()
except(KeyboardInterrupt):
        client_socket.close()
        server_socket.close()
    
