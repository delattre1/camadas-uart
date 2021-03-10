from enlace import *
import os
import time
import numpy as np
from utils import datagram_builder, receivement_handler
serialName = "/dev/ttyACM1"


class Servidor:
    def __init__(self,):
        self.com2 = enlace(serialName)
        self.com2.enable()
        self.finished_handshake = False
        self.contador_pacotes = 0
        self.pacotes_recebidos = []

    def waiting_handshake(self,):
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        self.rxLen = self.com2.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com2.rx.getBufferLen()

        print('recebeu algo')
        self.rxBuffer, self.nRx = self.com2.getData(self.rxLen)
        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)
        print(f'r_head: {self.r_head}\n')
        if self.r_eop == b''.join(is_available):
            pacote = datagram_builder(eop=is_available)
            self.com2.sendData(pacote)

            print(f'Handshake realizado,\nIniciando recepção dos pacotes...\n')
            self.finished_handshake = True
            self.com2.rx.clearBuffer()
            print(
                f'len buffer depois do handshake: {self.com2.rx.getBufferLen()}')

    def check_package_integrity(self,):
        tamanho_received_payload = len(self.r_payload)
        tamanho_pelo_header = list(self.r_head)[0]
        print(
            f'tamanho descrito no header: {tamanho_pelo_header} | recebido: {tamanho_received_payload}')
        is_len_ok = tamanho_received_payload == tamanho_pelo_header

        if is_len_ok:
            package = datagram_builder(resend=False)
            self.com2.sendData(package)
            print(
                f'O pacote [{self.contador_pacotes}] foi recebido com sucesso\n')
            self.contador_pacotes += 1
            self.pacotes_recebidos.append(self.r_payload)
        else:
            print(
                f'O pacote [{self.contador_pacotes}] veio errado, pedindo o reenvio')
            #package = datagram_builder(resend=True)
            # self.com2.sendData(package)

    def get_packages_and_store(self,):

        self.rxLen = self.com2.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com2.rx.getBufferLen()

        print(f'O tamanho do buffer é: {self.rxLen}')
        self.rxBuffer, self.nRx = self.com2.getData(self.rxLen)
        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        print(f'o tamanho do que chegou é: {self.nRx}')
        pause = input('press enter to continue')

        # self.check_package_integrity()

    def main(self,):
        print(f'Servidor Inicializado...\n')

        while not self.finished_handshake:
            self.waiting_handshake()

        os._exit(os.EX_OK)


servidor = Servidor()
servidor.main()
