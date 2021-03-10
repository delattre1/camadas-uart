import os
from enlace import *
import time
import sys
import numpy as np
from utils import datagram_builder, receivement_handler, open_image, separate_pacotes

#serialName = "/dev/ttyACM0"
serialName = "/dev/ttyVirtualS1"


class Client:
    def __init__(self, path):
        self.com1 = enlace(serialName)
        self.com1.enable()
        self.finished_handshake = False
        self.img_array = open_image(path)
        self.lista_pacotes = separate_pacotes(self.img_array)
        self.contador_pacotes = 0

    def send_package(self):
        self.com1.sendData(self.pacote)

    def receive_package(self):

        self.rxLen = self.com1.rx.getBufferLen()

        while self.rxLen == 0:
            self.rxLen = self.com1.rx.getBufferLen()

            self.elapsed_time = time.time() - self.start_time

            if self.elapsed_time >= 5:
                send_again = input('Time Out - Enviar novamente? (s/n)')
                if send_again == 's':
                    self.send_package()
                    time.sleep(1)
                    self.start_time = time.time()

                elif want_send_again == 'n':
                    print(f'finalizar client...')
                    os._exit(os.EX_OK)

        self.rxBuffer, self.nRx = self.com1.getData(self.rxLen)

        self.r_head, self.r_payload, self.r_eop = receivement_handler(
            self.rxBuffer)

        print(f'chegou {self.rxBuffer} com tamanho: {self.nRx}')
        len_from_header = list(self.r_head)[0]
        print(f'Tamanho de acordo com o header: {len_from_header}')

    def waiting_handshake(self,):
        print(f'Verificando estado do servidor...')
        is_available = [b'\x11', b'\x01', b'\x11', b'\x11']

        self.pacote = datagram_builder(eop=is_available)
        self.send_package()

        while not self.finished_handshake:
            elapsed_time = time.time() - self.start_time
            self.receive_package()

            if self.r_eop == b''.join(is_available):
                print(f'Handshake realizado,\nIniciando o envio dos pacotes...\n')
                self.finished_handshake = True

            elif elapsed_time >= 5:
                want_send_again = input(
                    'TIME OUT - Sem resposta servidor\nGostaria de mandar novamente? (s/n)')
                if want_send_again == 's':
                    self.send_package(pacote)
                    start_time = time.time()
                elif want_send_again == 'n':
                    print(f'finalizar client...')
                    os._exit(os.EX_OK)

    def main(self,):
        print(f'Client inicializado...\n')

        self.start_time = time.time()
        while not self.finished_handshake:
            self.waiting_handshake()

        print(f'Iniciando o envio dos pacotes...')

        os._exit(os.EX_OK)


client = Client('imgs/advice.png')
client.main()
