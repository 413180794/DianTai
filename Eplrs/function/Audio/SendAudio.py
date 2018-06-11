import socket
import pyaudio


class SendAudio(object):

    CHUNK = 160
    FORMAT = pyaudio.paInt8
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 10000
    with open('IP.config') as IPtxt:
        IP = str(IPtxt.read().split("=")[1])

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.addr = (SendAudio.IP, 20000)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recoder(self):
        stream = self.p.open(format=SendAudio.FORMAT,
                        channels=SendAudio.CHANNELS,
                        rate=SendAudio.RATE,
                        input=True,
                        frames_per_buffer=SendAudio.CHUNK,
                             )
        while True:
            data = stream.read(SendAudio.CHUNK, exception_on_overflow=False)
            print("send------------------"+ str(data))
            self.s.sendto(data, self.addr)
            # print(lend(data))


