# by ARTRoyale (A. Lebedev) for ZapRoyale

import socket
import sys
import zlib
import time

#тут коннектимся к хосту и порту
server_address = ('artroyalecppapp.ddns.net', 9339)
mock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# пишем что все ок
print("Podklucheno!",server_address[0],'on port',server_address[1])
mock.connect(server_address)
print('Podklucheno!')


# проверяем, прошел ли коннект
while 1:
    
    message = 
    try:
        mock.sendall(message)
# это если все хуево
    except:
        print('ERROR: vse ploho!')
        print('Pizdets cherez 15 sekund...')
        time.sleep(15)
        quit()
    print('Message Sent. Awaiting Response.')
    data = mock.recv(4096)
    zdata = str(data)[2:-1]
    sresp = zdata
