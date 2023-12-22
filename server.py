
import socket
import threading
import sys
import argparse

# debug vars
debug_mode = 0

# cli vars
port = ""
start = False
host_ip = socket.gethostbyname(socket.gethostname())

client_list = []
number_of_clients = 0

# init socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def client_input_thread(client_t, username, dm):
    # thread function to handle input from a single client
    while True:
        try:
            # receive message from client
            message = client_t.recv(20480).decode()
            
            if message:
                if debug_mode:
                    print(message)
                    sys.stdout.flush()
                
                str = message
                
                if message == ":Exit":
                    str = username + " left the chatroom"
                    print(str)
                    sys.stdout.flush()
                    for other_client in client_list:
                        other_client.send(str.encode())
                    client_t.close()
                    client_list.remove(client_t)
                    return
                
                print(str)
                sys.stdout.flush()
                
                # Log the received message (optional)
                with open("server_log.txt", "a") as log_file:
                    log_file.write(str + "\n")
                
                for other_client in client_list:
                    if other_client != client_t:
                        other_client.send(str.encode())
            else:
                continue
        except Exception as e:
            print(f"Error occurred: {e}")
            client_list.remove(client_t)
            client_t.close()
            return
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int)
    parser.add_argument('-start', action='store_true')
    args = parser.parse_args()
    
    port = args.port
    start = args.start
    
    server.bind((host_ip, port))
    server.listen(20)
    
    if debug_mode:
        print(port, start)
        sys.stdout.flush()
        
    print(f"Server started on port {args.port}. Accepting connections")
    sys.stdout.flush()
    
    while True:
        #accept client connection
        client, address = server.accept()
        
        passcode_reply = "true"
        client.send(passcode_reply.encode())
        
        if passcode_reply == "false":
            # remove connection
            client.close()
            continue
        
        # send message in server and to other clients that new user joined
        client_username = client.recv(20480).decode()
        str_to_send = client_username + " joined the chatroom"
        print(str_to_send)
        sys.stdout.flush()
        
        for other_client in client_list:
            if debug_mode:
                print(other_client)
                print(str_to_send)
                sys.stdout.flush()
            try:
                other_client.send(str_to_send.encode())
            except:
                continue
        
        # append to list and create new thread
        client_list.append(client)
        ++number_of_clients
        client_thread = threading.Thread(target = client_input_thread, args = (client, client_username, number_of_clients))
        client_thread.start()
        
        if debug_mode:
            print(f"new thread # {number_of_clients} started")
            sys.stdout.flush()
    
    server.close()
