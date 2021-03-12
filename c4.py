from enlace import *
import os
import time
import numpy as np
from utils import datagram_builder, receivement_handler, open_image, separate_packages

serialName = "/dev/ttyVirtualS1"


class Client:
    def __init__(self, path):
        self.com1 = enlace(serialName)
        self.com1.enable()
        self.img_array = open_image(path)
        self.l_bytes_img = separate_packages(self.img_array)

    def make_datagrams_from_image(self):
        # for each lits of bytes, it creates a datagram and store in a list
        self.list_size = len(self.l_bytes_img)
        self.datagrams_list = [
            datagram_builder(
                payload=self.l_bytes_img[i], current_package=i, total_of_packages=self.list_size)
            for i in range(self.list_size)]

    def send_package(self):
        self.com1.sendData(self.package)

    def get_header(self):
        self.r_header, self.len_r_header = self.com1.getData(10)

    def get_payload_eop(self):
        package_header = list(self.r_header)
        package_size = package_header[0]

        # header[3 e 4] representam o tamanho
        bytes_total_packages = self.r_header[3:5]
        self.number_of_packages = int.from_bytes(bytes_total_packages, 'big')

        # header[1 e 2] representam o pacote atual
        bytes_current_package = self.r_header[1:3]
        self.current_package = int.from_bytes(bytes_current_package, 'big')

        self.r_package, self.len_r_package = self.com1.getData(package_size)
        self.r_payload = self.r_package[:-4]
        self.r_eop = self.r_package[-4:]
        #print(f'payload: {self.r_payload} | eop: {self.r_eop}')

    def receive_handshake(self):
        self.get_header()
        self.get_payload_eop()

    def send_handshake(self):
        print(f'Verificando estado do servidor...')

        self.package = datagram_builder(server_available=True)
        self.send_package()

        self.start_time = time.time()
        while self.com1.rx.getBufferLen() == 0:
            self.time_delta = time.time() - self.start_time
            if self.time_delta >= 4:
                should_send_again = input(
                    'Didn"t receive response. Send again? (s/n) ')
                if should_send_again == 's':
                    print(f'Enviando novamente...\n')
                    self.send_package()
                    self.start_time = time.time()
                else:
                    os._exit(os.EX_OK)

        self.receive_handshake()

        if list(self.r_header)[5] == 255:
            print(f'Resposta recebida - server ready\n')

    def send_image(self):
        self.make_datagrams_from_image()
        contador = 0
        for datagram in self.datagrams_list:
            self.package = datagram
            self.send_package()
            print(
                f'Enviando o pacote n: [{contador}/{self.list_size -1}]')
            contador += 1
            time.sleep(0.0001)

        print(f'Finalizando client')

    def main(self,):
        print(f'Client inicializado...\n')

        self.send_handshake()

        print(f'Iniciando o envio dos pacotes...')

        self.send_image()
        time.sleep(1)
        os._exit(os.EX_OK)


client = Client('imgs/advice.png')
client.main()
