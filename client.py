import socket
import os
# Change to your Localhost/LAN IP address (same as server.py)
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
                client.sendall(b"<<EOF>>")  # end of file marker
                print(client.recv(1024).decode().strip())
                continue

            # Download command
            if cmd.startswith("download "):
                filename = cmd.split(maxsplit=1)[1]
                client.sendall(cmd.encode())  # send download <filename>
                with open(filename, 'wb') as f:
                    while True:
                        chunk = client.recv(1024)
                        if b"<<EOF>>" in chunk:
                            f.write(chunk.replace(b"<<EOF>>", b""))
                            break
                        f.write(chunk)
                print("Downloaded successfully.")
                continue
            

            client.sendall(cmd.encode())
            response = client.recv(1024).decode()
            print(response.strip())
            if cmd=="mydir":
                items = os.listdir(Current_Directory)
                print("\n".join(items) )
    except KeyboardInterrupt:
        print("\n[!] Disconnected from server.")
    finally:    
        client.close()

if __name__ == "__main__":
    start_client()
