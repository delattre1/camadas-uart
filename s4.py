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

    def get_header(self):
        self.r_header, self.len_r_header = self.com2.getData(10)

    def get_payload_eop(self):
        package_header = list(self.r_header)
        package_size = package_header[0]
        # print(f'head: {self.r_header[2:4]}')

        # header[3 e 4] representam o tamanho
        bytes_total_packages = self.r_header[3:5]
        self.number_of_packages = int.from_bytes(bytes_total_packages, 'big')

        # header[1 e 2] representam o pacote atual
        bytes_current_package = self.r_header[1:3]
        self.current_package = int.from_bytes(bytes_current_package, 'big')

        self.r_package, self.len_r_package = self.com2.getData(package_size)
        self.r_payload = self.r_package[:-4]
        self.r_eop = self.r_package[-4:]

        # print(f'payload: {self.r_payload} | eop: {self.r_eop}')

    def receive_handshake(self):
        self.get_header()
        self.get_payload_eop()

        # print(f'header recebido as list: {list(self.r_header)}')

        if list(self.r_header)[5] == 255:
            print(f'Respondendo o client - server ready\n')
            time.sleep(1)
            self.send_handshake()

    def send_handshake(self):
        self.package = datagram_builder(server_available=True)
        self.send_package()

    def receive_image(self):
        received_entire_img = False
        self.r_payloads = []
        self.num_last_package = 0

        while not received_entire_img:
            self.get_header()
            self.get_payload_eop()
            self.r_payloads.append(self.r_payload)

            # verificar se o pacote atual é igual ao anterior +1
            self.is_next_package = self.num_last_package + 1 == self.current_package
            self.is_eop_right = self.r_eop == b'\xff\xff\xff\xff'

            if self.is_next_package and self.is_eop_right:
                self.num_last_package = self.current_package

            print(f'Recebeu o proximo? [{self.is_next_package}]', end=' | ')
            print(f'Is eop ok?  [{self.is_eop_right}]', end=" | ")
            print(
                f'Received package [{self.current_package} / {self.number_of_packages}]')

            self.send_response()

            if (self.number_of_packages) == self.current_package:
                received_entire_img = True
                print(f'Received all packages')

        self.juntar_imagem()

    def send_finished(self):
        self.package = datagram_builder(finished=True)
        self.send_package()
        print(f'Todos os pacotes chegaram...\nAvisando o client e finalizando comunicação')

    def send_response(self):

        if self.is_eop_right and self.is_next_package:
            self.package = datagram_builder(acknowledge=True)
        else:
            self.com2.rx.clearBuffer()
            self.package = datagram_builder(acknowledge=False)
            print(f'Solicitando pacote [{self.num_last_package+1}]...')

        self.send_package()

    def juntar_imagem(self):
        received_img = b''.join(self.r_payloads)

        with open('imagem-recebida.png', 'wb') as file:
            file.write(received_img)

        print(f'Imagem salva...\n')

    def main(self,):
        print(f'Servidor Inicializado...\n')
        self.receive_handshake()

        self.receive_image()
        self.send_finished()
        time.sleep(1)
        self.com2.disable()
        os._exit(os.EX_OK)


servidor = Servidor()
servidor.main()
