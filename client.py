import socket    
import numpy as np      
import cv2 
import time
from PIL import Image
import pickle
from getmac import get_mac_address

def main(read=False):
    cached_macs = []

    # Checks Cached MAC Addresses
    with open("cached-mac-addrs.txt", "r") as f:
        content = f.read()
        cached_macs = content.split("\n")
    
    print("Cached MAC Addrs: ", cached_macs)


    s = socket.socket()    
    
    host = "192.168.0.209"
    port = 12345  

    try:
        s.connect((host, port)) 
    except:
        print("Connection Failed")
        exit()

    server_mac = get_mac_address(ip=host)
    print(f"Successfully Connected to {host}:{port}")
    print("Server MAC Address: ", server_mac)

    # Conditionally Adds To Cached MAC Addrs
    if server_mac not in cached_macs:
        f = open("cached-mac-addrs.txt", "a")
        f.write('\n' + server_mac)
        f.close()


    while True:
        msg = input("Enter Message: ")
        s.send(msg.encode()) 

        if msg == "return":
            returned_msg = s.recv(2048)
            print("Recieved: " + returned_msg.decode())
        
        elif msg == "screen":
            handle_screen_request(s)
        
        elif msg == "disconnect":
            print("Disconnecting...")
            break

        elif msg == "exit":
            s.close()
            break
    
    s.close()
    print("Connection Termination Successful")


# Handles The Recieving of Screen Data From the Server
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
    main(True)