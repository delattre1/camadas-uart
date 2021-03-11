from enlace import *
import os
import time
import numpy as np
from utils import datagram_builder, receivement_handler, open_image

serialName = "/dev/ttyVirtualS1"


class Client:
    def __init__(self, path):
        self.com1 = enlace(serialName)
        self.com1.enable()
        self.img_array = open_image(path)

    def send_package(self):
        self.com1.sendData(self.package)

    def get_header(self):
        self.r_header, self.len_r_header = self.com1.getData(10)

    def get_payload_eop(self):
        package_size = list(self.r_header)[0]
        self.r_package, self.len_r_package = self.com1.getData(package_size)
        self.r_payload = self.r_package[:-4]
        self.r_eop = self.r_package[-4:]
        print(f'payload: {self.r_payload} | eop: {self.r_eop}')

    def receive_handshake(self):
        self.get_header()
        self.get_payload_eop()

    def send_handshake(self):
        print(f'Verificando estado do servidor...')

        self.package = datagram_builder(server_available=True)
        self.send_package()

        self.receive_handshake()

        if list(self.r_header)[3] == bytes([255]):
            print(f'Resposta recebida - server ready\n')
            self.send_handshake()

    def main(self,):
        print(f'Client inicializado...\n')

        self.send_handshake()

        print(f'Iniciando o envio dos pacotes...')

        os._exit(os.EX_OK)


client = Client('imgs/advice.png')
client.main()
