# by ARTRoyale (A. Lebedev) for ZapRoyale

import socket
import threading
import struct
import os
import uuid
import random

# начинаем дебаг
global debugmode
debugmode = True
def debug(debmessage):
    if debmessage:
        if debugmode:
            print('[DEBUG]',debmessage)
        else:
            pass
    else:
        pass
def randomBytes(n):
    return bytes(random.getrandbits(8) for i in range(n))
def mockrcv(mock):
    rdata = mock.recv(10086)
    if not rdata:
        return "nulldata"
    return rdata

def serverlisten(mock, client):
    ndata=mockrcv(mock)
    if(ndata=="nulldata"):
        print('[WARNING] Net proksi!')
        return False
    else:
        lmessage_id = int(str(struct.unpack('>H', ndata[:2]))[1:-2])
        if (lmessage_id >= 30000 or lmessage_id < 10000):
            lmessage_id = 'Neizvestniy messadzh'
        elif len(str(lmessage_id)) is not 5:
            lmessage_id = 'Neizvestniy messadzh'
        print('[OK] Servak => Proksi', lmessage_id)
        response = ndata
        try:
            client.send(response)
        except ConnectionAbortedError:
            client.close()
            debug('closed')
            
global gl_server_address
gl_server_address = ('***.***.*.**', 9339) 

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print('[OK] Zapusk Proksi')

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print('[INFO] Klient => Proksi', address, 'podklucheno')
            client.settimeout(60) #таймаут
            mock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[INFO] Proksi =><= Server pudkluchen k",gl_server_address[0],'on port',gl_server_address[1])
            mock.connect(gl_server_address)
            print('[INFO] Proksi =><= Server podkluchen')
            threading.Thread(target = self.listenToClient,args = (client,address,mock)).start()

    def listenToClient(self, client, address, mock):
        while True:
            try:
                data = client.recv(4098)
            except:
                debug('closed')
                mock.close()
            try:
                message_id = int(str(struct.unpack('>H', data[:2]))[1:-2])
            except:
                message_id = 'Neizvestniy messadzh'
            try:
                if (message_id >= 30000 or message_id < 10000):
                    message_id = 'Neizvestniy messadzh'
            except:
                message_id = 'Neizvestniy messadzh'
            try:
                if len(str(message_id)) is not 5:
                    message_id = 'Neizvestniy messadzh'
            except:
                message_id = 'Neizvestniy messadzh'

            print('[OK] Klient => Proksi', message_id)
            fmessage = data
            try:
                mock.sendall(fmessage)
            except:
                debug('done closing?')
                break
            print('[OK] Proksi => Server', message_id)
            while 1:
                debug('Slushayu servak')
                r = serverlisten(mock, client);
                if r == False:
                    debug('Net infy ot servaka')
                    break
                else:
                    debug('Danniye polucheny ot servaka')
                    break

if __name__ == "__main__":
    port_num = 9339
    print('[INFO] Proksi podkluchaetsa k portu', port_num)
    ThreadedServer('0.0.0.0',port_num).listen()
