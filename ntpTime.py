import socket
import struct
import sys
import time

def RequestTimefromNtp(addr='0.es.pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return time.ctime(t), t

if __name__ == "__main__":
    print(RequestTimefromNtp())
    print(RequestTimefromNtp('1.es.pool.ntp.org'))
    print(RequestTimefromNtp('2.es.pool.ntp.org'))
    print(RequestTimefromNtp('3.es.pool.ntp.org'))