# ./server.out --port=2000 [--debug]
# python3 Server.py --port=2000
# python3 parapate_bhuang69Client_part2.py --id="Leon" --port=3000 --server="127.0.0.1:2000"
# python3 parapate_bhuang69Client_part2.py --id="Ada" --port=4000 --server="127.0.0.1:2000"

import socket
import argparse
import sys

server_ip = "127.0.0.1"

users = {

}

def parse_arguments():
    parser = argparse.ArgumentParser(description="TCP Chat Client")
    parser.add_argument("--port", type=int, help="Port number for incoming chat requests")
    args = parser.parse_args()

    if not (args.port):
        print("Missing required arguments.")
        sys.exit(1)
    return args.port

def getID(response):
    _, client_id = response.splitlines()[1].split(':')
    client_id = client_id.strip()

    return client_id

def getPort(response):

    _, client_port = response.splitlines()[3].split(':')
    client_port = client_port.strip()

    return client_port

def main():

    try:

        firstBridge = True

        server_port = int(parse_arguments())
        print("Server is listening on 127.0.0.1:" + str(server_port))

        while True:

            # REGISTER
            # create ACK socket
            reg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            reg_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            reg_socket.bind((server_ip, server_port))
            reg_socket.listen()

            reg_conn, _ = reg_socket.accept()

            # get ACK
            reg_response = reg_conn.recv(1024).decode()
            reg_client_id = getID(reg_response)
            reg_client_port = getPort(reg_response)

            # building REGACK Header
            reg_header = f"REGISTER\r\n"
            reg_header += f"clientID: {reg_client_id}\r\n"
            reg_header += f"IP: {server_ip}\r\n"
            reg_header += f"Port: {reg_client_port}\r\n\r\n"

            if reg_response == reg_header:
                regack_header = f"REGACK\r\n"
                regack_header += f"clientID: {reg_client_id}\r\n"
                regack_header += f"IP: {server_ip}\r\n"
                regack_header += f"Port: {reg_client_port}\r\n\r\n"

                print("REGISTER: " + str(reg_client_id) + " from " + str(server_ip) + ":" + str(reg_client_port) + " received")

                users.update({reg_client_id : reg_client_port})

                reg_conn.send(regack_header.encode())

            reg_conn.close()
            reg_socket.close()


            # BRIDGE
            # building first ACK Header
            if firstBridge:
                # create ACK socket
                br_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                br_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                br_socket.bind((server_ip, server_port))
                br_socket.listen()

                br_conn, _ = br_socket.accept()

                # get ACK
                response = br_conn.recv(1024).decode()
                br_client_id = getID(response)

                first_client_id = None

                first_bridge_header = f"BRIDGE\r\n"
                first_bridge_header += f"clientID: {br_client_id}\r\n\r\n"
                if response == first_bridge_header:
                    empty = f"BRIDGEACK\r\n"
                    empty += f"clientID: \r\n"
                    empty += f"IP: \r\n"
                    empty += f"Port: \r\n\r\n"

                    print("BRIDGE  : " + str(br_client_id) + " " + str(server_ip) + ":" + str(users[br_client_id]))

                    first_client_id = br_client_id

                    br_conn.send(empty.encode())

                    firstBridge = False

                br_conn.close()
                br_socket.close()
            
            
            if not firstBridge:
                # REGISTER
                # create ACK socket
                regbr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                regbr_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                regbr_socket.bind((server_ip, server_port))
                regbr_socket.listen()

                regbr_conn, _ = regbr_socket.accept()

                # get ACK
                regbr_response = regbr_conn.recv(1024).decode()
                regbr_client_id = getID(regbr_response)
                regbr_client_port = getPort(regbr_response)

                # building REGACK Header
                regbr_header = f"REGISTER\r\n"
                regbr_header += f"clientID: {regbr_client_id}\r\n"
                regbr_header += f"IP: {server_ip}\r\n"
                regbr_header += f"Port: {regbr_client_port}\r\n\r\n"


                if regbr_response == regbr_header:
                    regackbr_header = f"REGACK\r\n"
                    regackbr_header += f"clientID: {regbr_client_id}\r\n"
                    regackbr_header += f"IP: {server_ip}\r\n"
                    regackbr_header += f"Port: {regbr_client_port}\r\n\r\n"

                    print("REGISTER: " + str(regbr_client_id) + " from " + str(server_ip) + ":" + str(regbr_client_port) + " received")

                    users.update({regbr_client_id : regbr_client_port})

                    regbr_conn.send(regackbr_header.encode())

                regbr_conn.close()
                regbr_socket.close()

                # create ACK socket
                br_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                br_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                br_socket.bind((server_ip, server_port))
                br_socket.listen()

                br_conn, _ = br_socket.accept()

                # get ACK
                response = br_conn.recv(1024).decode()
                br_client_id = getID(response)

                # building ACK header
                bridge_header = f"BRIDGE\r\n"
                bridge_header += f"clientID: {br_client_id}\r\n\r\n"

                # building BRIDGEACK Header
                bridgeack_header = f"REGISTER\r\n"
                bridgeack_header += f"clientID: {br_client_id}\r\n"
                bridgeack_header += f"IP: {server_ip}\r\n"
                bridgeack_header += f"Port: {users[br_client_id]}\r\n\r\n"

                if response == bridge_header:

                    print("BRIDGE " + str(first_client_id) + " " + str(server_ip) + str(users[first_client_id]) + " " + str(br_client_id) + " " + str(server_ip) + str(users[br_client_id]))

                    br_conn.send(regack_header.encode())
                
                br_conn.close()
                br_socket.close()

            br_conn.close()
            br_socket.close()

    except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
