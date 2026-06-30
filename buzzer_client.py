import socket
import sys
import threading
import time
from socket import error as socket_error

HOST = "192.168.25.209"
PORT = 10000


class MessageSendThread(threading.Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.daemon = True

    def run(self):
        try:
            while True:
                message = input("Send Message \nex) 'buzzer,do' ~ 'buzzer,ti' >> ")

                if message.lower() == "exit":
                    print("Client exit")
                    self.sock.close()
                    break

                message = message.strip() + "\n"
                self.sock.sendall(message.encode("utf-8"))

        except Exception as err:
            print(err)


class ClientSocket:
    def __init__(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = (HOST, PORT)

                print(f"This is Client. connecting IP: {server_address[0]} PORT: {server_address[1]}")
                self.sock.connect(server_address)

                send_thread = MessageSendThread(self.sock)
                send_thread.start()

                while True:
                    data = self.sock.recv(4096)

                    if data:
                        print("\n[Server]: " + data.decode("utf-8"))
                    else:
                        print("Disconnect")
                        break

            except socket_error as serr:
                print(serr)
                time.sleep(3)

            except Exception as err:
                print(err)

            finally:
                print("Closing socket")
                try:
                    self.sock.close()
                except:
                    pass


if __name__ == "__main__":
    try:
        ClientSocket()

    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()