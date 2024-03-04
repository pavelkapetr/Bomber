import socket


def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000
    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(1)
    print(f"Listening on {server_ip}:{port}")
    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # communication loop
    while True:
        # data od klienta v surové binární podobě - musíme dekódovat
        request = client_socket.recv(1024)
        request = request.decode("utf-8")

        if request.lower() == "close":
            # client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        response = "accepted".encode("utf-8")
        # client_socket.send(response)

    client_socket.close()
    print("Connection to client closed")
    server.close()


run_server()
