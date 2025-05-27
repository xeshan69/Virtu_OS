import socket
import os
SERVER_IP = '192.168.0.108'  
PORT = 8200
Current_Directory = os.getcwd()
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    welcome = client.recv(1024).decode()
    print(welcome.strip())
    try: 
        while True:
            cmd = input(">> ")
            if cmd.lower() in ["exit", "quit"]:
                break
            # Upload command
            if cmd.startswith("upload "):
                filename = cmd.split(maxsplit=1)[1]
                if not os.path.exists(filename):
                    print("File not found.")
                    continue

                client.sendall(cmd.encode())  # send upload <filename>
                with open(filename, 'rb') as f:
                    while chunk := f.read(1024):
                        client.sendall(chunk)
                client.sendall(b"")  # end of file marker
                print(client.recv(1024).decode().strip())
                conti