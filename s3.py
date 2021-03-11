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
        self.finished_handshake = False
        self.contador_pacotes = 0
        self.pacotes_recebidos = []

    def send_package(self):
        self.com2.sendData(self.pacote)
        print(f'Acabei de enviar um pacote com :{len(self.pacote)}bytes...\n')

    def receive_package(self):
        # funcao para recebimento de pacotes, incluindo verificacao se pacote chegou corretamente
        self.rxLen = self.com2.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com2.rx.getBufferLen()

        self.rxBuffer, self.nRx = self.com2.getData(self.rxLen)

        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        # print(f'chegou {self.rxBuffer} com tamanho: {self.nRx}')
        len_from_header = list(self.r_head)[0]
        must_resend = list(self.r_head)[2]
        print(
            f'Tamanho de acordo com o header: {len_from_header}\nChegou: {self.nRx}\n')

        if must_resend == 22:
            print('Foi solicitado o reenvio...\n')
            self.sendData()
            self.receive_package()

        elif len_from_header != (self.nRx):  # pacote recebido nao está correto
            print(f'Solicitando pacote novamente\n')
            self.pacote = datagram_builder(resend=True)
            self.send_package()
            self.receive_package()

    def waiting_handshake(self,):
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']
        self.pacote = datagram_builder(eop=is_available)
        self.receive_package()

        if self.r_eop == b''.join(is_available):

            print(f'Handshake realizado,\nIniciando recepção dos pacotes...\n')
            self.send_package()
            # sleep to client receive data, else is geting error :p
            time.sleep(1)
            self.finished_handshake = True

    def main(self,):
        print(f'Servidor Inicializado...\n')

        while not self.finished_handshake:
            self.waiting_handshake()

        os._exit(os.EX_OK)


servidor = Servidor()
servidor.main()
