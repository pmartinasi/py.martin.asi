from multiprocessing import Process
import os
import random

def f(cmdIN):
    os.system(str(cmdIN))

if __name__ == '__main__':
    processrow = []
    for i in range(256):
        ip_txt = '192.168.1.' + str(i)
        pingstr = 'ping ' + ip_txt + ' -l 1024 -n 32 -l 1024'
        print(pingstr)
        p = Process(target=f, args=(pingstr,))
        processrow.append(p)
    for p in processrow:
        p.start()
    for p in processrow:
        p.join()