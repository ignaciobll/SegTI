import socket
import sys
from thread import *
from xtea import *

############# XTEA ##############

key = " "*16

x = new(key, mode=MODE_OFB, IV="12345678")


#################################


HOST = 'localhost'
PORT = 4443

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created...'

try:
    s.bind((HOST, PORT))
    print 'Socket binded...'
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


s.listen(5)
print 'Socket listening...'


def client_thread(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break

        (key, iv, text) = data.decode().strip('\n').split('\t')
        
        response = ""
        
        if key != "" and text != "":
            if correct_params(key, iv):
                x = new(key, mode=MODE_OFB, IV=iv)
                response = x.encrypt(text)
                print "\tReceived: " + text

        conn.sendall(response)


def correct_params(key, iv):
    return len(key) == 16 and len(iv) == 8

while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(client_thread, (conn, ))

s.close()
print 'Closed socket.'
