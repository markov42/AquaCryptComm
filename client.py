import socket
import threading
import sys
import argparse
from leader import Leader
from follower import Follower

debug_mode = 0
port = ""
host = ""
username = ""
join = False
mode = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def receive_server_message(client_t, dm, mode):
    while True:
        try:
            recv_message = client_t.recv(20480).decode()
            print(recv_message)
            if mode == "Follower":
                follower = Follower(recv_message.strip())
                recv_message = follower.getDecodedCommand()

            if recv_message:
                print(recv_message)
                sys.stdout.flush()
            else:
                continue
        except:
            continue

def send_message(client_t, dm, mode):
    while True:
        try:
            message = sys.stdin.readline()
            
            if mode == "Leader":
                leader = Leader(message.strip())
                message = leader.getEncodedCommand()

            if message:
                with open("message.txt", "w") as file:
                    file.write(message)
                    
                if message == ":Exit":
                    print(f"You: {message.strip()}")
                    client_t.send(message.encode())
                    client_t.close()
                    exit()
                    return
                else:
                    print(f"You: {message.strip()}")
                    client_t.send(message.encode())
                    continue
            else:
                continue
        except:
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', type=str)
    parser.add_argument('-username', type=str)
    parser.add_argument('-port', type=int)
    parser.add_argument('-join', action='store_true')
    parser.add_argument('-mode', type=str, choices=["Leader", "Follower"], required=True)
    args = parser.parse_args()
    
    port = args.port
    host = args.host
    username = args.username
    join = args.join
    mode = args.mode

    if debug_mode:
        print(port, host, username, join)
        sys.stdout.flush()
        
    # establish connection to the server
    client.connect((host, port))
    
    # check if you can connect
    pass_check = client.recv(1024)
    if pass_check.decode() == "true":
        print(f"Connected to {host} on port {port}")
        sys.stdout.flush()
    else:
        # if incorrect, close connection and exit
        print("Cannot connect to the server")
        sys.stdout.flush()
        client.close()
        exit()
    
    # send username to server
    client.send(username.encode())
    
    # Correctly passing the mode argument to the threaded functions
    recv_thread = threading.Thread(target=receive_server_message, args=(client, 0, mode))
    recv_thread.start()
    send_thread = threading.Thread(target=send_message, args=(client, 0, mode))
    send_thread.start()
    
    #exit()
