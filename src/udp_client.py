# UDP client
import socket
import logging
import argparse

from util import construieste_mesaj_raw
from udp_server import calculeaza_checksum

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)


def send_message(address, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        logging.info('Trimitem mesajul "%s" catre %s:%d', message, address[0], address[1])
        sock.sendto(message.encode('utf-8'), address)

        logging.info('Asteptam un raspuns...')
        data, server = sock.recvfrom(4096)
        logging.info('Content primit: "%s"', data)

        # Calculam checksum pentru pachetul primit
        ip, port = sock.getsockname()
        print ip
        data_raw = construieste_mesaj_raw(server[0], ip, server[1], port, data)
        checksum_value = calculeaza_checksum(data)
        checksum_value = hex(checksum_value)

        logging.info('Checksum-ul calculat pentru %s este %s', data, str(checksum_value))
    finally:
        logging.info('closing socket')
        sock.close()


def main():
    parser = argparse.ArgumentParser(description='Client UDP',
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--server', '-s', dest='server', action='store',
                        required=True, help='Adresa IP a serverului')
    parser.add_argument('--port', '-p', dest='port', action='store', type=int,
                        required=True, help='Portul serverului.')
    parser.add_argument('--mesaj', '-m', dest='mesaj', action='store',
                        default="", help='Mesaj de trimis prin UDP')
    args = parser.parse_args()
    server_address = (args.server, args.port)

    send_message(server_address, args.mesaj)


if __name__ == '__main__':
    main()
