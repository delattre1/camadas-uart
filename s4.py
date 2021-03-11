from enlace import *
import os
import time
import numpy as np
from utils import datagram_builder, receivement_handler

serialName = "/dev/ttyVirtualS0"

# quando o client precisa enviar novamente, o servidor encerra sem avisar o client


class Servidor:
    def __init__(self,):
        self.com2 = enlace(serialName)
        self.com2.enable()

    def send_package(self):
        self.com2.sendData(self.package)
        print(f'Acabei de enviar um pacote com :{len(self.pacote)}bytes...\n')

    def get_header(self):
        self.r_header, self.len_r_header = self.com2.getData(10)

    def get_payload_eop(self):
        package_size = list(self.r_header)[0]
        self.r_package, self.len_r_package = self.com2.getData(package_size)
        self.r_payload = self.r_package[:-4]
        self.r_eop = self.r_package[-4:]
        print(f'payload: {self.r_payload} | eop: {self.r_eop}')

    def receive_handshake(self):
        self.get_header()
        self.get_payload_eop()

        if list(self.r_header)[3] == bytes([255]):
            print(f'Respondendo o client - server ready\n')
            self.send_handshake()

    def send_handshake(self):
        self.package = datagram_builder(server_available=True)
        self.send_package()

    def main(self,):
        print(f'Servidor Inicializado...\n')
        self.receive_handshake()
        os._exit(os.EX_OK)


servidor = Servidor()
servidor.main()
