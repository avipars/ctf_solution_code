import socket

"""
Sample program to connect to the exe socket server and interact with it
"""


def main():
    """
    Assuming that you already did the port-scan before you run this script (so you know the server port)
    """
    s_ip = input(
        "Enter the server IP or N to use default: "
    )  # (change based on result of port-scan)
    if s_ip in {"N", "n"}:
        s_ip = "127.0.0.1"

    # (change based on result of port-scan)
    s_port = int(input("Enter the server port: "))

    c_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM)  # client socket

    try:
        c_socket.connect((s_ip, s_port))
        user_input = ""
        proceed = True

        while (
            user_input != "EXIT" and proceed
        ):  # exit if typed EXIT or server closes connection

            data = c_socket.recv(1024).decode()

            if not data or data.strip().lower() == "exit":
                print("Server has closed the connection")
                proceed = False
                break

            print(f"Server: {data}")

            user_input = input("Client: ")
            res = c_socket.send(user_input.encode())
            if res <= 0:  # something went wrong
                print("Server has closed the connection")
                proceed = False

    except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError) as e:
        print(f"Server Error: {e}")
    except Exception as e:
        print(f"Client Error: {e}")
    finally:
        print("Closing client")
        c_socket.close()


if __name__ == "__main__":
    main()
