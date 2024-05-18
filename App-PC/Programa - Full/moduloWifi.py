# Importação das bibliotecas necessárias
import time  # Biblioteca para manipulação de tempo
import socket  # Biblioteca para comunicação via socket
import json  # Biblioteca para manipulação de arquivos json
import threading  # Biblioteca para criação de threads
from queue import Queue  # Biblioteca para criação de filas


class InMessage:  # Incoming Message definition
    def __init__(self, data, require_ack: bool, client_addr: str) -> None:  # Constructor
        self.data = data  # The data received
        self.require_acknowledgment = require_ack  # If the message requires an acknowledgment
        self.client_addr = client_addr  # The client address


class OutMessage:  # Outgoing Message definition
    def __init__(self, data: str, require_ack: bool = False) -> None:  # Constructor
        self.data = data  # The data to be sent


class WiFiCommunicator:  # WiFi Communicator class
    ACKNOWLEDGMENT_FLAG = 'A'  # Acknowledgment flag
    CPU_RELEASE_SLEEP = 0.000_001  # CPU release sleep time

    # Function to create the WiFi Communicator
    # @param max_buffer_sz: The maximum amount of bytes to be received at once
    # @param port: The port on which we shall communicate
    # @param in_queue_sz: The incoming messages' queue size, if 0 -> infinite
    # @param out_queue_sz: The outgoing messages' queue size, if 0 -> infinite
    def __init__(self, max_buffer_sz: int, port: int = 11111, in_queue_sz: int = 0, out_queue_sz: int = 0) -> None:
        assert max_buffer_sz > 0, f"Buffer size must be > 0 [{max_buffer_sz = }]"
        assert in_queue_sz >= 0, f"Queue size can't be negative [{in_queue_sz = }]"
        assert out_queue_sz >= 0, f"Queue size can't be negative [{out_queue_sz = }]"
        self._rip = False  # Rest in peace flag
        self._have_client = False  # Have client flag
        self._max_buffer_size = max_buffer_sz  # The maximum amount of bytes to be received at once
        self._incoming_messages_queue = Queue(maxsize=in_queue_sz)  # Incoming messages queue
        self._outgoing_messages_queue = Queue(maxsize=out_queue_sz)  # Outgoing messages queue
        # Client info
        self._client = None  # The client socket
        self._client_address = None  # The client address
        # Socket creation
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow the socket to be reused
        soc.bind(('0.0.0.0', port))  # Bind to the port
        soc.listen(0)  # Now wait for client connection.
        # Start the show
        self._threads = [
            threading.Thread(target=self.__listener_thread, daemon=True),  # The listener thread
            threading.Thread(target=self.__sender_thread, daemon=True),  # The sender thread
            threading.Thread(target=self.__wait_for_connection_thread, daemon=True, args=[soc]),
            # The connection thread
        ]
        for thread in self._threads:
            thread.start()  # Start the thread

    # Function to get a message from the incoming messages queue
    # @return InMessage: The incoming message
    def get_message(self) -> InMessage:
        return self._incoming_messages_queue.get()

    # Function to send a message
    # @param message: The message to be sent
    def send_message(self, message: OutMessage) -> None:
        self._outgoing_messages_queue.put(message)

    # Function to destroy the communicator (stop the threads and close the socket)
    def destroy(self):
        if self._client is not None:  # If we have a client
            self._client.close()  # Close the client socket
        self._rip = True  # Set the RIP flag
        for thread in self._threads:  # For each thread
            thread.join(0.1)  # Wait for the thread to finish

    # Function to wait for a connection
    # @param soc: The socket
    def __wait_for_connection_thread(self, soc: socket.socket) -> None:
        self._client, self._client_address = soc.accept()  # Establish connection with client.
        self._have_client = True  # We have a client

    # Function to decode the incoming message
    # @param in_bytes: The incoming bytes
    # @return InMessage: The incoming message
    def __decode(self, in_bytes: bytes) -> 'None|InMessage':
        message = in_bytes.decode()  # Decode the bytes
        if not len(message):  # If the message is empty
            return None  # Return None
        ack = message[0] == self.ACKNOWLEDGMENT_FLAG  # Check if the message requires an acknowledgment
        data = message[1 * ack:]  # Get the data
        return InMessage(data=data, require_ack=ack, client_addr=self._client_address)  # Return the incoming message

    # Function to listen for incoming messages
    def __listener_thread(self):
        while not self._rip:  # While we're not dead
            if not self._have_client:  # If we don't have a client
                time.sleep(self.CPU_RELEASE_SLEEP)  # Sleep
                continue
            message = self._client.recv(self._max_buffer_size)  # Receive the message
            decoded_msg = self.__decode(message)  # Decode the message
            if decoded_msg is not None:  # If the message is not None
                self._incoming_messages_queue.put(decoded_msg)  # Put the message in the incoming messages queue

    # Function to encode the outgoing message
    # @param message: The outgoing message
    # @return bytes: The encoded message
    def __encode(self, message: OutMessage) -> bytes:
        return message.data.encode()  # Encode the message

    # Function to send the outgoing messages
    def __sender_thread(self):
        while not self._rip:  # While we're not dead
            if not self._have_client:  # If we don't have a client
                time.sleep(self.CPU_RELEASE_SLEEP)  # Sleep
                continue
            # This is blocking on purpose, if not, we'd have to handle getting no-data when timing-out
            msg = self._outgoing_messages_queue.get()  # Get the outgoing message
            self._client.send(self.__encode(msg))  # Send the message

    # Função para ler os dados disponíveis na porta serial
    def read_wifi_data(self, debug="n"):  # Função para ler os dados disponíveis na porta serial
        while not self._rip:
            if self._incoming_messages_queue.empty():
                time.sleep(self.CPU_RELEASE_SLEEP)
                dataout = None
                return dataout
            else:
                datain = self.get_message()  # Lê a linha disponível
                if datain.require_acknowledgment:
                    msg = OutMessage(data='A')
                    self.send_message(msg)
                if debug == "s":
                    print("Wifi - data:", datain)  # Imprime a mensagem recebida no terminal para debug
                jdata = json.loads(str(datain.data, 'utf-8'))  # Converte a resposta para json
                dataout = [(jdata["Item1"]), (jdata["Item2"]), (jdata["Item3"]), (jdata["Item4"]),
                           (jdata["Item5"]), (jdata["Item6"])]
                if debug == "s":
                    print("Wifi - data:", dataout)  # Imprime a mensagem recebida no terminal para debug
                return dataout


if __name__ == "__main__":  # O código abaixo será executado apenas quando este arquivo for executado diretamente
    pass  # Nada acontece
