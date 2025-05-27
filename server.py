import socket
import threading
import os

BASE_DIR = os.path.abspath("server_storage")

HOST='192.168.0.108' # Change to your Localhost/LAN IP address
PORT=8200

def handle_client(conn, addr):
    print(f"[+] Handling client {addr}")
    conn.sendall(b"Welcome to the server!\n")
    current_dir = BASE_DIR
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            cmd_parts = data.split()
            if not cmd_parts:
                continue

            cmd = cmd_parts[0]
            args = cmd_parts[1:]

            if cmd == "ls":
                items = os.listdir(current_dir)
                response = "\n".join(items) or "Directory is empty."

            elif cmd == "mkdir" and args:
                folder = args[0]
                if ".." in folder:
                    response = "Invalid folder name."
                else:
                    path = os.path.join(current_dir, folder)
                    os.makedirs(path, exist_ok=True)
                    response = f"Folder '{folder}' created."

            elif cmd == "touch" and args:
                filename = args[0]
                if ".." in filename:
                    response = "Invalid filename."
                else:
                    path = os.path.join(current_dir, filename)
                    open(path, 'a').close()
                    response = f"File '{filename}' created."

            elif cmd == "cd" and args:
                folder = args[0]
                new_path = os.path.join(current_dir, folder)
                new_path = os.path.abspath(new_path)

                if not new_path.startswith(BASE_DIR):
                    response = "Access denied."
                elif os.path.isdir(new_path):
                    current_dir = new_path
                    response = f"Moved to '{folder}'."
                else:
                    response = "Directory not found."

            elif cmd == "pwd":
                relative_path = os.path.relpath(current_dir, BASE_DIR)
                response = "/" if relative_path == "." else f"/{relative_path}"

            elif cmd in ["exit", "quit"]:
                response = "Goodbye!"
                conn.sendall(response.encode())
                break
            
                # # Additional commands can be added here
            elif cmd == "rm" and args:
                item = args[0]
                if ".." in item:
                    response = "Invalid item name."
                else:
                    path = os.path.join(current_dir, item)
                    if os.path.isfile(path):
                        os.remove(path)
                        response = f"File '{item}' deleted."
                    elif os.path.isdir(path):
                        os.rmdir(path)
                        response = f"Directory '{item}' deleted."
                    else:
                        response = "Item not found."

            elif cmd == "upload" and args:
                filename = args[0]
                path = os.path.join(current_dir, filename)
                with open(path, 'wb') as f:
                    while True:
                        chunk = conn.recv(1024)
                        if b"<<EOF>>" in chunk:
                            f.write(chunk.replace(b"<<EOF>>", b""))
                            break
                        f.write(chunk)
                response = f"Uploaded '{filename}' successfully."

            elif cmd == "download" and args:
                filename = args[0]
                path = os.path.join(current_dir, filename)
                
                if os.path.isfile(path):
                    with open(path, 'rb') as f:
                        while chunk := f.read(1024):
                            conn.sendall(chunk)
                    conn.sendall(b"<<EOF>>")
                    continue  # skip sending text response
                else:
                    response = "File not found."
            elif cmd == "mydir":
                response="Client's current directory contents:\n"
            else:
                response = "Unknown command."

            conn.sendall((response + "\n").encode())
        except Exception as e:
                print(f"Error: {e}")
                break
        
    conn.close()
    print(f"[-] Connection closed for {addr}")

def server():
    print(f"[+] Base directory set to: {os.path.abspath("server_storage")}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[+] Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"[+] Connection from {addr}")
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server()