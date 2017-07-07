#!/usr/bin/env python

''' module to forward messages from input file to addressants in separetade packets. Remember that one messages could be addressed to many addressants'''

import os
import sys
import re
import json
import threading
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import scapy.all as scapy
import getter
from itertools import izip  # just zip in python 3.x

# global constants

FILE_PATH = sys.argv[1]
IVASYK_PATTERN = '(.{2})+$'  #line has an even quantity of symbols
DMYTRYK_PATTERN = '^[A-Z]'  # line starts with head letter
LESYA_PATTERN = ' end$'  # line ends with ' end'
IVASYK = 'IVASYK'
DMYTRYK = 'DMYTRYK'
OSTAP = 'OSTAP'
LESYA = 'LESYA'
JSON_FILE_PATH = 'servers.json'
PORT = 8888
TIMEOUT = 2

contacts = (IVASYK, DMYTRYK, OSTAP, LESYA)

ADDR_DICT = {}

receivers = {contact: [] for contact in contacts}  # containt class objects


class Addressant:

    ''' this class will contain a information about user '''

    packets = []

    def __init__(self, name, ip):
        self.__name = name
        self.__ip = ip

    def __ping(self):

        ''' function which check if a receiver is online and return boolean'''

        ans, unans = scapy.sr(scapy.IP(dst=self.__ip)/scapy.ICMP(), timeout=TIMEOUT, verbose=False)
        return bool(ans)

    def __sniffing_udp(self, packet, line):

        ''' function check if a packet was sent '''

        catched = scapy.sniff(filter='udp and port 8888', timeout=TIMEOUT)
        for pckt in catched:
            try:
                msg = pckt.getlayer(scapy.Raw).load  # get a encode Raw
                msg_to_check = msg.decode('utf-8', 'ignore')  # decode a Raw
                if self.__ip == pckt.getlayer(scapy.IP).dst and line == msg_to_check:
                    print('sended successfully\n')  # it will be printed a lot times, sorry
            except AttributeError:  # kostil'
                pass

    def send_packet(self):

        ''' function send all packets line by line to a receiver '''

        for line in self.packets:
            if (self.__ping()):
                packet_to_send = scapy.IP(dst=self.__ip)/scapy.UDP(sport=PORT, dport=PORT)/line
                thread = threading.Thread(target=self.__sniffing_udp, args=(packet_to_send, line, )).start()
                scapy.send(packet_to_send, verbose=False)
            else:
                print("do not response:", self.__ip)


def check_args():

    ''' this function needs to check numbers of arguments from command line'''

    if len(sys.argv) != 2:
        print("please run the program in this way:\n")
        print("sudo python home_work#1 txt_file.txt")
        exit(1)


def exists_check(path):

    '''here we check if file exists'''

    try:
        os.path.exists(path)
    except FileNotFoundError:
        print("Not exists: exit\n")
        exit(1)


def make_class_obj(json_file_path='servers.json'):

    ''' make a class objects using json file '''

    exists_check(json_file_path)
    with open(json_file_path) as json_file:
        ADDR_DICT = json.load(json_file)  # fill a dict with name as key and ip as content
    for server, contact in izip(ADDR_DICT, contacts):
        receivers[contact].append(Addressant(server, ADDR_DICT[server]))  # creating a class objects


def check_ivasyk(line):

    '''here we check @line for IVASYK and return a boolean'''

    return (re.match(IVASYK_PATTERN, line))


def check_dmytryk(line):

    '''here we check @line for DMYTRYK and return a boolean'''

    return (not check_ivasyk(line) and re.match(DMYTRYK_PATTERN, line))


def check_lesya(line):

    '''here we check @line for LESYA and return a boolean'''

    return (re.match(LESYA_PATTERN, line))


def forward_messages(path):

    '''here we will forward each line to the correct key in dictionary(class object)'''

    all_messages = getter.get_msg(path).splitlines()
    all_messages = [x.strip('\n') for x in all_messages]
    for line in all_messages:
        if line == '\n':
            continue
        elif check_lesya(line):
            for obj in receivers[LESYA]:  # this loop just for get to the class object
                obj.packets.append(line)
        elif check_ivasyk(line):
            for obj in receivers[IVASYK]:
                obj.packets.append(line)
        elif check_dmytryk(line):
            for obj in receivers[DMYTRYK]:
                obj.packets.append(line)
        else:
            for obj in receivers[OSTAP]:
                obj.packets.append(line)


def main():
    check_args()
    exists_check(FILE_PATH)
    make_class_obj(JSON_FILE_PATH)
    forward_messages(FILE_PATH)
    for contact in receivers:
        for obj in receivers[contact]:
            obj.send_packet()

if __name__ == "__main__":
    main()
