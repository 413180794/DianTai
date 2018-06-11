import socket
import threading

import pyaudio
from enum import Enum, unique


telephoneNumber={

    "13856756894":"192.168.1.10",
    "18612240136" : "127.0.0.1",

}

@unique
class ConstValue(Enum):
    CHUNK = 10   # 发送 或者 接受 1024字节 （音频数据） 数据用打印出来后每一字节用两位16进制表示
    FORMAT = pyaudio.paInt8
    CHANNELS = 1 # 通道数量
    AUDIOPROT = 20000
    WATCHPROT = 20001
    RATE = 16000
    with open('localIP') as IPtxt:
        IP = str(IPtxt.read().split("=")[1])

class Telephone(object):  #  电话类 模拟通话功能

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.audiosocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # 每一个类只需要一个
        self.ifcommunicate = 0  # 是否在通话中，如果正在通话中，则为1，否则为0.
        self.watchsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # 用来管理信令的UDP
        self.allowcommunicate = False # 默认不允许通话，需要经过判断来开启这个功能
        self.AudioAddress = (ConstValue.IP.value,ConstValue.AUDIOPROT.value)
        self.WatchAddress = (ConstValue.IP.value, ConstValue.WATCHPROT.value)
        self.stream = self.p.open(format=ConstValue.FORMAT.value,
                             channels=ConstValue.CHANNELS.value,
                             rate=ConstValue.RATE.value,
                             input=True,
                             frames_per_buffer=ConstValue.CHUNK.value,
                             )
        t = threading.Thread(target=self._watchudp)
        t.start()


    def _watchudp(self):  # 等待发送而来的信令
        self.watchsocket.bind(self.WatchAddress)
        while True:
            xlmessage, orginaddr = self.watchsocket.recvfrom(2048)  # 发送而来的信令
            print(xlmessage) # 若收到的是\x01 ，之后判断ifcommunicate是否为1
            if xlmessage == b'\x01' and self.ifcommunicate == 1:
                self.watchsocket.sendto('\x02'.encode('utf-8'), orginaddr)
                # 若收到的是\x01 ，之后判断ifcommunicate是否为1，如果正在通话返回信令00000010
            if xlmessage == b'\x01' and self.ifcommunicate == 0:
                # 若收到的是\x01 ，之后判断ifcommunicate是否为0，允许通话返回信令00000011
                self.watchsocket.sendto('\x03'.encode('utf-8'), orginaddr)
            if xlmessage == b'\x02':
                print("用户正忙")
                self.allowcommunicate = False
                # return  检测线程没必要停掉，用户正忙的状态下做出相应的响应就可以
            if xlmessage == b'\x03': # 若收到00000011 则允许通话
                print("允许通话")
                self.allowcommunicate = True




    def _receiveaudio(self): # 等待发送而来的语音信息
        return


    def sendaudio(self): # 要求输入电话号码，号码对应着同一子网下目标的ip地址
        telephonenumber = input("请输入号码:")

        try:
            wantIP = telephoneNumber[telephonenumber]    # 取得目的电台的IP地址
            # watchaddress = (wantIP, ConstValue.WATCHPROT.value)    # 将IP地址与端口号绑定起来
            self.watchsocket.sendto('\x01'.encode('utf-8'), (wantIP, ConstValue.WATCHPROT.value))
            print(1)
        except KeyError as keyerror:
            print("不存在该号码")
        # 接着按下拨号键发送信令 设置IP。拨打键:发送信令00000001 此时应该有一个专门的UDP线程用来单独处理信令。这一个UDP线程应该在初始化中完成
        print(2)
        print(self.allowcommunicate)
        while True:
            if self.allowcommunicate == True:
                audiodata = self.stream.read(ConstValue.CHUNK.value, exception_on_overflow=False)
                newaudiodata = '\x04'.encode('utf-8')+audiodata
                print(newaudiodata)
                if newaudiodata.startswith(b'\x04'):
                    print(12312)
                self.audiosocket.sendto(newaudiodata, (wantIP, ConstValue.AUDIOPROT.value))
                if self.allowcommunicate == False: # 一方中断通话
                    return
                # print(lend(data))

if __name__ == '__main__':
    a = Telephone()
    a.sendaudio()



