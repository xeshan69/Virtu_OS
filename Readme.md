VirtuOS: LAN-Based Virtual Operating System
Project Description

VirtuOS is a simple LAN-based virtual operating system implemented in Python, demonstrating client-server communication for basic file system operations. It allows a client to connect to a server running on a local network and perform common commands such as listing directories, changing directories, creating/removing files and folders, and managing local directory views. Additionally, it supports uploading files from the client to the server and downloading files from the server to the client.

This project is ideal for understanding fundamental network programming concepts using sockets and implementing remote file system interactions.
Features

    Client-Server Architecture: Connects clients to a central server over a Local Area Network (LAN).
    Remote File System Operations:
        ls: List contents of the current directory on the server.
        cd <directory>: Change the current working directory on the server.
        mkdir <directory>: Create a new directory on the server.
        rm <file_or_directory>: Remove a file or an empty directory on the server.
        touch <file>: Create an empty file on the server.
    Local Client Directory View:
        mydir: Displays the current working directory of the client's local machine.
    File Transfer:
        upload <local_file> <server_path>: Uploads a file from the client's local machine to the server.
        download <server_file> <local_path>: Downloads a file from the server to the client's local machine.
    Robust Error Handling: Basic error handling for invalid commands, file not found, permission denied, etc.

How to Run
Prerequisites

    Python 3.x installed on both server and client machines.
    All machines must be on the same Local Area Network (LAN).

1. Server Setup (server.py)

    Save the Server File:
    Save your server code as server.py in a dedicated directory. This directory will be the server's root for file operations.

    Configure Server IP and Port:
    Open server.py and ensure the HOST variable is set to '0.0.0.0' to listen on all available network interfaces, and choose a PORT (e.g., 12345).
    Python

# Example snippet from server.py
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345      # Choose an available port above 1024

Run the Server:
Open a terminal or command prompt, navigate to the directory where server.py is saved, and run:
Bash

    python server.py

    The server will start listening for incoming connections. Note down the server's IP address (the IP of the machine running server.py on your LAN) that clients will connect to. You can find your LAN IP using ip a (Linux), ifconfig (macOS/Linux), or ipconfig (Windows).

2. Client Setup (client.py)

    Save the Client File:
    Save your client code as client.py in a separate directory on a client machine. This directory will be the client's root for mydir and file transfer operations.

    Configure Server IP and Port:
    Open client.py and set SERVER_HOST to the IP address of the machine running server.py (obtained in the server setup step) and SERVER_PORT to the same port as configured in server.py.
    Python

# Example snippet from client.py
SERVER_HOST = 'YOUR_SERVER_LAN_IP' # e.g., '192.168.1.100'
SERVER_PORT = 12345                 # Must match server's port

Run the Client:
Open a terminal or command prompt, navigate to the directory where client.py is saved, and run:
Bash

    python client.py

    The client will attempt to connect to the server. Upon successful connection, you will see a prompt (e.g., VirtuOS>) where you can enter commands.

Client Commands

Once connected, you can use the following commands at the VirtuOS> prompt:

    ls: Lists the files and directories in the current working directory on the server.
    cd <directory_name>: Changes the current working directory on the server.
        cd ..: Move up one directory level.
        cd /: Go to the server's root directory.
    mkdir <directory_name>: Creates a new directory with the specified name in the current server directory.
    rm <file_or_directory_name>: Removes a file or an empty directory from the server.
        Caution: This command does not typically confirm deletion. Use with care.
    touch <file_name>: Creates an empty file with the specified name in the current server directory.
    mydir: Displays the current working directory of the client's local machine. This command operates only on the client side.
    upload <local_file_path> [server_destination_path]: Uploads a file from the client's local machine to the server.
        local_file_path: The path to the file on the client's machine (can be relative to the client's CWD).
        server_destination_path (optional): The path on the server where the file should be saved. If omitted, the file will be uploaded to the server's current directory with its original name.
    download <server_file_path> [local_destination_path]: Downloads a file from the server to the client's local machine.
        server_file_path: The path to the file on the server.
        local_destination_path (optional): The path on the client where the file should be saved. If omitted, the file will be downloaded to the client's current directory with its original name.
    help: Displays a list of available commands.
    exit / quit: Disconnects the client from the server and exits the client application.

Project Structure (Conceptual)

VirtuOS/
├── server.py
├── client.py
└── server_files/ # (Optional) Initial directory for server's root operations
    ├── some_file.txt
    └── some_folder/
        └── another_file.log

Technologies Used

    Python 3.x: Core programming language.
    socket module: For network communication (TCP sockets).
    os module: For interacting with the operating system's file system (server-side).
    threading module (Server-side): To handle multiple client connections concurrently.