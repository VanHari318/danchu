import threading
import socket
import os
import argparse
import sys
import tkinter as tk

from PIL.ImageOps import expand
from pyexpat.errors import messages
from wheel.macosx_libfile import swap32


class Send(threading.Thread):
    '''listens for user input from command line
        sock the connected sock object
        name (str): the user'''
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """listen for user input from the command line
            typing "Quit" will close the connecttion"""
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            #type "quit", leave the chatroom
            if message == 'Quit':
                self.sock.sendall('Server: {} has been left the chat'.format(self.name).encode('utf-8'))
                break
            #send message to server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('utf-8'))
        print('\nQuitting...')
        self.sock.close()
        sys.exit(0)

class Receive(threading.Thread):
    #listening for incoming messages from the server
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        #receive data from the server and display it in the gui
        while True:
            message = self.sock.recv(1024).decode('utf-8')
            if message:
                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end='')
                else:
                    print('\r{}\n{}: '.format(message, self.name), end='')
            else:
                print('\nNo. We have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                sys.exit(0)


class Client:
    #management of client-server connecttion and integration of GUI
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None
    def start(self):
        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfull to connect to {}:{}...'.format(self.host, self.port))
        print()
        #self.name = input('Youre name: ')
        print()
        print('Welcome, {}! Getting ready to send and recevie messages...'.format(self.name))

        #create sen and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        #start send and recieve thread
        send.start()
        receive.start()

        self.sock.sendall('Server: {} has been joined the chat. Say whatsup!'.format(self.name).encode('utf-8'))
        print("\rReady! Leave the chat room anytime by typing 'Quit'\n'")
        print('{}: '.format(self.name), end='')
        return receive


    def send(self, textInput):
        #sends textInput data from the GUI
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))
        #typing Quit to leave the chatroom
        if message == 'Quit':
            self.sock.sendall('Server: {} has leave the chat'.format(self.name).encode('utf-8'))
            print('\nQuitting...')
            self.sock.close()
            sys.exit(0)

        #send message to the server for broadcasting
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('utf-8'))


def main(host, port, name):
    #initialize and run GUI application
    client = Client(host, port)
    client.name = name
    receive = client.start()

    window = tk.Tk()
    window.title("Chatroom")
    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    receive.messages = messages
    fromMessage.grid(row= 0, column=0, columnspan=2, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda x: client.send(textInput))
    textInput.insert(0, "Write your message here.")

    btnSend = tk.Button(
        master=window,
        text='Send',
        command=lambda : client.send(textInput)

    )

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, padx=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')
    parser.add_argument('-n', '--name', required=True, help='Your username for the chatroom')
    args = parser.parse_args()
    main(args.host, args.p, args.name)








