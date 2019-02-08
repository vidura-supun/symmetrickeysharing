#!/usr/bin/python
import hashlib
import socket
import threading
from cryptography.fernet import Fernet
import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


answer = input("Choose an option~\nClient or Server : ").lower()
print("\nEnter 'exit' to quit\n")

if(answer == 'server'):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65433        # Port to listen on (non-privileged ports are > 1023)
    print('Listening. . .')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        
        def handle_client(client_socket):
            de_message = Fernet(bytes(input("Enter the secret key: "), 'utf8')) 
            while True:
                # print out what the client sends
                data = de_message.decrypt(client_socket.recv(1024))

                #seperating message and the hash
                mess = data.decode("utf-8")[0:len(data.decode("utf-8"))-64]
                sha_hash = data.decode("utf-8")[len(data.decode("utf-8"))-64:]
                
                
                print("[*] Received: %s" % mess)
                #re hashing for comparison
                sha_hash2 = hashlib.sha256(bytes(mess, 'utf8')).hexdigest()
                print("\nIntegrity Verificaion....")
                if(sha_hash==sha_hash2):
                    print("~VERIFIED~")
                else:
                    print("Verification Failed")
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

    #secret key sending via email
    fromaddr = input("enter your email address : ") 
    password = getpass.getpass("enter your password : ")
    toaddr = input("enter recievers email address : ")
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    sub = "Your Secret Key from " + fromaddr

    msg['Subject'] = sub
 
    body = "--Start of key--\n" + key.decode("utf-8") + "\n--End of key--"
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("email sent succesfully!") 


    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65433        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while(True):
            message = input("\nEnter message: ") 
            #hashing of the message and adding it to the message
            n_message = message + hashlib.sha256(bytes(message, 'utf8')).hexdigest()
            cli_rep = cipher_suite.encrypt(bytes(n_message, 'utf8'))
            
            
            
            
            #print(cipher_suite.decrypt(cli_rep).decode("utf-8"))
            if(cipher_suite.decrypt(cli_rep) == b'exit'):
                break
            else:
                s.sendall(cli_rep)
              
                data = s.recv(1024)
                print('\nSuccess')




