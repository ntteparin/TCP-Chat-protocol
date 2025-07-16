# ./server.out --port=2000 [--debug]
# python3 Server.py --port=2000
# python3 Client.py --id="Leon" --port=3000 --server="127.0.0.1:2000"
# python3 Client.py --id="Ada" --port=4000 --server="127.0.0.1:2000"

import socket
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Chat Client")
    parser.add_argument("--id", type=str, help="Client ID")
    parser.add_argument("--port", type=int, help="Port number for incoming chat requests")
    parser.add_argument("--server", type=str, help="Server IP address and port number")
    args = parser.parse_args()

    if not (args.id and args.port and args.server):
        print("Missing required arguments.")
        sys.exit(1)

    return args.id, args.port, args.server

def send_message(sock, message):
    sock.send(message.encode())

def receive_message(sock):
    return sock.recv(1024).decode()

def parse_response(response):
    lines = response.split('\n')
    response_type = lines[0]

    if response_type == "REGACK":
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(': ')
                headers[key] = value
        return response_type, headers
    elif response_type == "BRIDGEACK":
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(': ')
                headers[key] = value
        return response_type, headers
    elif response_type == "QUIT":
        return response_type, None
    else:
        return None, None

def register_client(client_socket, client_id, client_port):
    message = f"REGISTER\nclientID: {client_id}\nIP: localhost\nPort: {client_port}"
    send_message(client_socket, message)
    response = receive_message(client_socket)
    response_type, headers = parse_response(response)
    if response_type == "REGACK":
        print("Registration successful.")
    else:
        print("Registration failed. Server response:", response)

def request_bridge(client_socket, client_id):
    message = f"BRIDGE\nclientID: {client_id}"
    send_message(client_socket, message)
    response = receive_message(client_socket)
    response_type, headers = parse_response(response)
    if response_type == "BRIDGEACK":
        print("Bridge request successful. Friend's contact information:", headers)
    else:
        print("Bridge request failed. Server response:", response)

def main():

    try:
        client_id, client_port, server_address = parse_arguments()
        server_ip, server_port = server_address.split(':')

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, int(server_port)))
        print(client_id + " running on " + server_ip)
        while True:
            user_input = input().strip()

            if user_input == '/id':
                print("Client ID:", client_id)
            elif user_input == '/register':
                register_client(client_socket, client_id, client_port)
            elif user_input == '/bridge':
                request_bridge(client_socket, client_id)
            elif user_input == '/quit':
                print("Exiting...")
                send_message(client_socket, "QUIT")
                break

    except KeyboardInterrupt:
            print("Program terminated.")

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
