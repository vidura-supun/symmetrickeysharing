#!/usr/bin/python
import socket
import threading

answer = input("Choose an option~\nClient or Server : ").lower()

if(answer == 'server'):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    print('Listening. . .')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        
        def handle_client(client_socket):
            while True:
                # print out what the client sends
                data = client_socket.recv(1024)
                print("[*] Received: %s" % data)
                #send back a packet
                client_socket.send("ACK!".encode())
       
        while(True):
            client,addr = s.accept()
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.start()

if(answer == 'client'):
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(True):
            
            cli_rep = input("Enter your message: ")
            if(cli_rep == 'exit'):
                break
            else:
                s.sendall(cli_rep.encode())
                data = s.recv(1024)
                print('Received', repr(data))




