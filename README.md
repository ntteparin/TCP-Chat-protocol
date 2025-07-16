# TCP Chat Application

This is a simple TCP-based chat system consisting of a central server and multiple clients. Clients can register with the server and initiate peer-to-peer chat sessions.

## Files

- `Server.py` – The central server that keeps track of connected clients.
- `Client.py` – A client that can register with the server and chat with other registered clients.

## Requirements

- Python 3

## How to Run

### Start the Server

```bash
python3 Server.py --port=2000
```

- `--port`: Port number the server will listen on.

### Start a Client

```bash
python3 Client.py --id="Leon" --port=3000 --server="127.0.0.1:2000"
```

- `--id`: A unique identifier for the client.
- `--port`: Port number on which the client listens for chat connections.
- `--server`: Address and port of the central server to register with.

Start multiple clients with different IDs and ports:

```bash
python3 Client.py --id="Ada" --port=4000 --server="127.0.0.1:2000"
```

## Slash Commands

Clients can use the following `/` commands after launching the program:

| Command         | Description |
|----------------|-------------|
| `/register`    | Registers the client with the central server using the provided ID and port. Must be run before using other commands. |
| `/bridge`      | Initiates a direct peer-to-peer connection (a “bridge”) with another client. |
| `/id`          | Displays the current client’s ID. |
| `/quit`        | Gracefully exits the chat client. |

## Features

- Clients register themselves with the server.
- Clients can discover and initiate chat connections with each other.
- Peer-to-peer communication is enabled via TCP sockets.

## Notes

- Ensure each client uses a **unique port** and **ID**.
- The server must be running before any clients attempt to connect.
- You can run everything locally using `127.0.0.1` for testing.
