from enlace import *
import time
import numpy as np
from utils import datagram_builder, receivement_handler
serialName = "/dev/ttyACM1"


class Servidor:
    def __init__(self,):
        self.com2 = enlace(serialName)
        self.com2.enable()
        self.finished_handshake = False

    def is_waiting_handshake(self,):
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        self.rxLen = self.com2.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com2.rx.getBufferLen()
        print('recebeu algo')
        self.rxBuffer, self.nRx = self.com2.getData(self.rxLen)
        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)
        print(self.r_eop)
        if self.r_eop == b''.join(is_available):
            pacote = datagram_builder(eop=is_available)
            self.com2.sendData(pacote)

            print(f'Handshake realizado,\nIniciando recepção dos pacotes...\n')
            self.finished_handshake = True

    def main(self,):
        print(f'Servidor Inicializado...\n')

        while not self.finished_handshake:
            self.is_waiting_handshake()

        while True:

            print('esperando um pacotinho com sucesso')
            break
           # self.rxLen=com2.rx.getBufferLen()
           # while self.rxLen == 0:
           #     self.rxLen=com2.rx.getBufferLen()

           # self.rxBuffer, self.nRx=self.com2.getData(rxLen)
           # self.r_head, self.r_payload, self.r_eop=receivement_handler(
           # self.rxBuffer)


servidor = Servidor()
servidor.main()
