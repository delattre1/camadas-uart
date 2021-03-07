from enlace import *
import time
import numpy as np
from utils import datagram_builder, receivement_handler, open_image, separate_pacotes

serialName = "/dev/ttyACM0"


class Client:
    def __init__(self,):
        self.com1 = enlace(serialName)
        self.com1.enable()
        self.finished_handshake = False

    def is_waiting_handshake(self,):
        print(f'Iniciando handshake')
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        pacote = datagram_builder(eop=is_available)
        print(pacote)
        self.com1.sendData(pacote)
        print(f'Enviado pacote - handhake')

        self.rxLen = self.com1.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com1.rx.getBufferLen()

        self.rxBuffer, self.nRx = self.com1.getData(self.rxLen)

        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)
        if self.r_eop == is_available:
            print(f'Handshake realizado,\nIniciando o envio dos pacotes...\n')
            self.finished_handshake = True

    def main(self,):
        print(f'Client inicializado.\n')

        while not self.finished_handshake:
            self.is_waiting_handshake()

        while True:
            print('enviando os pacotinhos com sucesso')
            break


client = Client()
client.main()
