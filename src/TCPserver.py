#! /usr/bin/python3

import os
import sys
import socket
from colorziPython import pycolors



class TCPserver:

    def __init__(self):
        print(pycolors.WARNING + "-"*14, "Initializing File Transfering Protocol using TCP", "-"*14 + pycolors.ENDC + "\n")

        self.__getting_PORT()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                server.bind(("" , self.serverPort))
                server.listen(1)
            
            except socket.error as msg:
                print(f"Couldnt connect with the localhost with IP Address: 127.0.0.1\n{msg}\nTerminating program.")
                sys.exit(1)

            print("Server listening to. " + pycolors.FAIL + "Server " + pycolors.ENDC + f"---> 127.0.0.1" +  pycolors.FAIL + " Port " + pycolors.ENDC + f"---> {self.serverPort} |" + pycolors.OKGREEN + " CONNECTED\n" + pycolors.ENDC)

            self.__fileReciever(server)

        sys.exit(0)

        

    def __getting_PORT(self):
        try:
            self.serverPort = int(sys.argv[1])

            if len(sys.argv) > 2:
                raise IndexError

        except IndexError:
            print("Please Run program in following format'./ProgramName <Server PORT Number>' ...\nTerminating program.")
            sys.exit(1)

        except ValueError:
            print("Please Enter valid port Number...\nTerminating program.")
            sys.exit(1)


    def __fileReciever(self, server):
        
        try:
            senderSocket, Address = server.accept()

            print(f"... Incomming Connection from {Address[0]} |" + pycolors.OKGREEN + " CONNECTED" + pycolors.ENDC)

            fileRecv = senderSocket.recv(1024).decode('cp1252')

            fileName, fileSize = fileRecv.split("<SEPARATOR>")

            fileName = os.path.basename(fileName)
            fileSize = int(fileSize)

            with open(fileName, "wb") as file:

                while True:

                    recvByte = senderSocket.recv(1024)

                    if not recvByte:
                        break

                    file.write(recvByte)

            senderSocket.close()
            print("\nFile Recieved from " + pycolors.FAIL + "Server " + pycolors.ENDC + "-----> " + pycolors.WARNING + "IP: " + pycolors.ENDC + f"{Address} " + pycolors.WARNING + "PORT: " + pycolors.ENDC + f"{self.serverPort} |" + pycolors.OKGREEN + " SUCCESSFULLY" + pycolors.ENDC)

        except socket.error as msg:
            print("\nError Occured while recieving file " + "from " + pycolors.FAIL + "Client: " + pycolors.ENDC + f"\n{msg}\n\nTerminating program.")

        except Exception as exc:
            print("\nError Occured while Reading recieving file " + "from " + pycolors.FAIL + "Client: " + pycolors.ENDC + f"\n{exc}\n\nTerminating program.")



if __name__ == "__main__":

    __constructor = TCPserver()