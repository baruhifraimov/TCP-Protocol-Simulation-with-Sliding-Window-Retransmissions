import socket
import time

# setting variables for the Server's IP and port.
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345


def read_parameters_from_file(file_path):
    """
    Reads the message parameters from a file.
    """
    with open(file_path, 'r') as file:
        data = file.read()
    parameters = {}
    for line in data.splitlines():
        key, value = line.split(':', 1)
        parameters[key.strip()] = value.strip().strip('"')
    return parameters


def recv_message_with_boundary(client_socket):
    """
    Reads a message with a 4-byte length prefix.
    """
    try:
        length_prefix = client_socket.recv(4)
        if not length_prefix:
            print("Client closed the connection.")
            return None  # Connection closed by the client
        length_prefix = length_prefix.decode('utf-8')
        message_length = int(length_prefix)
        # Read the exact number of bytes for the message
        message = client_socket.recv(message_length).decode('utf-8')
        return message
    except ValueError:
        print("Error: Received an invalid message length prefix.")
        return None
    except ConnectionResetError:
        print("Connection was reset by the client.")
        return None


def start_server():
    """
    Starts the server and implements sliding window logic.
    """
    # Creating a socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding the socket to the address and the port of the server
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(2)  # a queue of 2 requests for any case

    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")

        # Getting the request from the client for the max-message-size
        data = client_socket.recv(1024).decode('utf-8')
        if data.startswith("MAX_SIZE_REQUEST"):
            # Get parameters from user or file
            source = input(
                "Enter 'file' to read MAX SIZE of the message from a file or 'input' to provide manually: ").strip().lower()
            if source == 'file':
                file_path = input("Enter the file path: ").strip()
                params = read_parameters_from_file(file_path)
                max_size = int(params['maximum_msg_size'])
            else:
                max_size = int(input("Enter the maximum message size: ").strip())

            client_socket.send(str(max_size).encode('utf-8'))

        # # Receive the sliding window size from the client
        # data = client_socket.recv(1024).decode('utf-8')
        # if data.startswith("WINDOW_SIZE:"):
        #     window_size = int(data.split(":")[1])
        #     print(f"Sliding window size received: {window_size}")

        received_messages = {}  # A list that stores out-of-order messages
        highest_contiguous_ack = -1  # saves the highest number of the packet that arrived correctly is sequence.

        while True:
            try:
                data = recv_message_with_boundary(client_socket)
                if data is None:
                    print("Client closed the connection. Exiting loop.")
                    break  # Exit the loop if the client closed the connection

                print(f"Received: {data}")
                try:
                    # Extract the message number and data
                    message_number, message_data = data.split(":", 1)
                    message_number = int(message_number)
                except ValueError:
                    print("Error parsing message.")
                    continue

                if message_number == highest_contiguous_ack + 1:
                    # Correct order, update highest_contiguous_ack
                    print(f"Message {message_number} arrived in the correct order: {message_data}")
                    highest_contiguous_ack = message_number

                    # Check for any buffered messages that can now be acknowledged
                    while highest_contiguous_ack + 1 in received_messages:
                        highest_contiguous_ack += 1
                        print(
                            f"Adding buffered message {highest_contiguous_ack}: {received_messages.pop(highest_contiguous_ack)}")

                    # Send a single ACK for the highest contiguous sequence number
                    ack_message = f"ACK{highest_contiguous_ack}"
                    client_socket.send(ack_message.encode('utf-8'))
                    print(f"Sent: {ack_message}")

                else:
                    # Out of order, store the message if not already stored
                    if message_number not in received_messages:
                        print(f"Message {message_number} out of order, storing: {message_data}")
                        received_messages[message_number] = message_data

                    # Resend the last valid ACK
                    ack_message = f"ACK{highest_contiguous_ack}"
                    client_socket.send(ack_message.encode('utf-8'))
                    print(f"Resent: {ack_message}")

            except ConnectionResetError:
                print("Connection was reset by the client. Exiting loop.")
                break  # Exit the loop if the connection is reset by the client
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
        print("Connection closed.")
        client_socket.close()


if __name__ == "__main__":
    start_server()
