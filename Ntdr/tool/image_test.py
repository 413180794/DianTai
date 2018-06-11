import hashlib
import os
import struct
from logging import getLogger

with open("../icons/group.png",'rb') as f:
    x = hashlib.md5(f.read()).hexdigest()
    print(type(x))
    print(x)


def getMd5OfFile(fname):
    if not os.path.exists(fname):
        return None
    with open(fname,'rb') as f:
        m = hashlib.md5()
        while True:
            d = f.read(10240)
            print(len(d))
            if not d:
                break
            m.update(d)
    return m.hexdigest()

def getFileSize(fname):
    size = os.path.getsize(fname)
    print(type(size))
    print(size)
    return size
print(getFileSize('../icons/group.png'))
print(getMd5OfFile('../icons/group.png'))

list = []

list.insert(2,3)
list.insert(0,1)
list.insert(1,2)
list.insert(3,4)
print(list)
'''
    while True:
        chunk_data = f.read(1024)
        x4 = chunk_data.decode('utf-8')
        print(x4)
        print(len(chunk_data))
        x= struct.pack('!1024s',chunk_data)
        print(x)
        if not chunk_data:
            break
        print(chunk_data)
        with open("x3.png",'ab') as f2:
            f2.write(chunk_data)
        with open("x4.png",'ab') as f3:
            x2 = struct.unpack('!1024s',x)

            f3.write(*x2z
'''