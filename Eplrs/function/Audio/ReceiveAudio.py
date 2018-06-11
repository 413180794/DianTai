import socket
import time
import pyaudio

# 接受语音数据的类
class ReceiveAudio(object):
    CHUNK = 1
    FORMAT = pyaudio.paInt8
    CHANNEL = 1
    RATE = 16000
    RECORD_SECONDS = 60
    with open('IP.config') as IPtxt:
        IP = str(IPtxt.read().split("=")[1])
    def __init__(self):
        self.address = (ReceiveAudio.IP, 20000)
        self.p = pyaudio.PyAudio()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(20)
        self.s.bind(self.address)
        self.s.setblocking(True)
        self.data = []


    def receive(self):
        stream = self.p.open(format=self.p.get_format_from_width(2),
                             channels=ReceiveAudio.CHANNEL,
                             rate=ReceiveAudio.RATE,
                             output=True
                             )
        while True:
            # try:
            data, addr = self.s.recvfrom(1024)
            print(data)
            if len(data) is not 0:
                stream.write(data)
            # except Exception as e:
            #     print("连接出错"+str(e))


