#! /usr/bin/python3

import os
import sys
import socket
from colorziPython import pycolors


class TCPclient:

    def __init__(self):
        print(pycolors.WARNING + "-"*14, "Initializing File Transfering Protocol using TCP", "-"*14 + pycolors.ENDC + "\n")

        self.__getting_IP_PORT_File()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        
            try:
                print(self.hostName, self.hostPort)
                client.connect((self.hostName , self.hostPort))

                print("Connection Established. " + pycolors.FAIL + "Server " + pycolors.ENDC + f"---> {self.hostName}" +  pycolors.FAIL + " Port " + pycolors.ENDC + f"---> {self.hostPort} |" + pycolors.OKGREEN + " CONNECTED" + pycolors.ENDC)

                self.__fileSender(client)

            except socket.error as msg:
                print(f"Couldnt connect with the server with IP Address: {self.hostName}\n{msg}\nTerminating program.")
                sys.exit(1)

        sys.exit(0)

        

    def __getting_IP_PORT_File(self):
        try:
            self.hostName = sys.argv[1]
            self.hostPort = int(sys.argv[2])
            self.fileName = sys.argv[3:]
            
            self.fileName = " ".join(self.fileName)

        except IndexError:
            print("Please Run program in following format'./ProgramName <Server IP Address> <Server PORT Number> <File Name>' ...\nTerminating program.")
            sys.exit(1)

        except ValueError:
            print("Please Enter valid port Number...\nTerminating program.")
            sys.exit(1)

        if os.path.exists(self.fileName) == False:
            print("Please Enter valid File...\nTerminating program.")
            sys.exit(1)


    def __fileSender(self, client):
        fileSize = os.path.getsize(self.fileName)
        SEPARATOR = "<SEPARATOR>"

        try:
            client.send(f"{os.path.basename(self.fileName)}{SEPARATOR}{fileSize}".encode("cp1252"))

            with open(self.fileName, 'rb') as file:
                while True:

                    curByte = file.read(4096)

                    if not curByte:
                        break

                    client.send(curByte)

            print("\nFile Transfered to " + pycolors.FAIL + "Server " + pycolors.ENDC + "-----> " + pycolors.WARNING + "IP: " + pycolors.ENDC + f"{self.hostName} " + pycolors.WARNING + "PORT: " + pycolors.ENDC + f"{self.hostPort} |" + pycolors.OKGREEN + " SUCCESSFULLY" + pycolors.ENDC)

        except socket.error as msg:
            print("\nError occured while sending file.. " +pycolors.WARNING + f"{self.fileName}" + pycolors.ENDC + " to server: " + pycolors.FAIL + f"{self.hostName}" + pycolors.ENDC + f"\n\n{msg}\nTerminating program.")



if __name__ == "__main__":
    
    __constructor = TCPclient()