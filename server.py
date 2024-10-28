import socket    
import numpy as np      
import cv2 
import time
from PIL import Image
import pickle
#import json

def main():
    s = socket.socket()                     

    host = "10.0.33.155"
    port = 12345  

    s.bind((host, port))         
    s.listen(1)  
    print(f"Server Listening on port {port}")   
            
    (client, addr) = s.accept() 
    print('Got connection from', addr)  

    while True: 
        msg = input("Enter Message: ")
        client.send(msg.encode()) 

        if msg == "return":
            returned_msg = client.recv(2048)
            print("Recieved: " + returned_msg.decode())
        
        elif msg == "screen":
            handle_screen_request(client)

        elif msg == "exit":
            client.close()
            break


def handle_screen_request(client):
    returned_msg = b''

    data_len = int(client.recv(1024).decode())
    print("Data Len: ", data_len)

    start_time = time.time()
    while len(returned_msg) < data_len:
        print("Incoming...")
        packet = client.recv(115200)
        returned_msg += packet

    end_time = time.time()
    print("Elapsed Time: ", end_time - start_time)


    img_width = 960
    #cv2.namedWindow("Screenshot", cv2.WINDOW_NORMAL)
    print("Converting Image...")
    [w, h, rgb] = pickle.loads(returned_msg)

    img = Image.frombytes("RGB", (w,h), rgb)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (img_width, int(1824/2736*img_width)))

    print("Showing Image...")

    cv2.imshow("Screenshot", img)

    cv2.waitKey(0)


if __name__ == "__main__":
    main()