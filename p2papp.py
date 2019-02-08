#!/usr/bin/python
import socket
import threading
from cryptography.fernet import Fernet


answer = input("Choose an option~\nClient or Server : ").lower()
print("\nEnter 'exit' to quit\n")

if(answer == 'server'):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    print('Listening. . .')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        
        def handle_client(client_socket):
            de_message = Fernet(bytes(input("Enter the secret key: "), 'utf8')) 
            while True:
                # print out what the client sends
                data = de_message.decrypt(client_socket.recv(1024))
                
                print("[*] Received: %s" % data.decode("utf-8"))
                #send back a packet
                client_socket.send("ACK!".encode())
       
        while(True):
            client,addr = s.accept()
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.start()

if(answer == 'client'):

    key = Fernet.generate_key() #generation of the key
    print("\nkey generated. . .\n\n--Start of key--\n" + key.decode("utf-8") + "\n--End of key--")

    cipher_suite = Fernet(key)

    #plain_text = cipher_suite.decrypt(b"gAAAAABcW-t3SP5NWJpJCMqHR1fkURoffr_6HAvqV_PAmag09Drtj9syhwuWvxiMOiUlEBfbWlUf1Zn1dp3FzUf3tn6E2vazrTvUXfUD78u_JqUFJ-RWysvk9Zv8mKHjLf-GGVC-w1cQ").decode("utf-8")

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(True):
            message = input("\nEnter message: ")
            cli_rep = cipher_suite.encrypt(bytes(message, 'utf8'))
            #print(cipher_suite.decrypt(cli_rep).decode("utf-8"))
            if(cipher_suite.decrypt(cli_rep) == b'exit'):
                break
            else:
                s.sendall(cli_rep)
              
                data = s.recv(1024)
                print('\nSuccess')




