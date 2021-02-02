from vidstream import StreamingServer
import threading
print("Hello there!")
#Mac 192.168.1.205
#RC 192.168.1.104

reciever = StreamingServer('192.168.1.205', 9999)

t = threading.Thread(target=reciever.start_server)
t.start()

while input("") != 'STOP':
    continue

reciever.stop_server()
