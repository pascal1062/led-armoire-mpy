import socket
import time

UDP_IP = "192.168.0.20" # Destination IP address
UDP_PORT = 47902      # Destination port
#MESSAGE = b"Hello, World!" # Message to send (must be bytes)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket
sock.settimeout(5)

'''
    lancer python3 et faire "import host_udp_send_recv"
    message example
    ("/esp32-LedCab/system/date-heure", "True")
    ("/esp32-LedCab/ledCab/value/get", "True")
    ("/esp32-LedCab/system/sunset/", "True")
    ("/esp32-LedCab/system/sunset/on", "True")
    ("/esp32-LedCab/system/exit", "True")
    ("/esp32-LedCab/ledCab/value/set", "255")
'''

while True:
    user_input = input("Enter message: ")
    MESSAGE = user_input.encode('utf-8')

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print("Message sent")

    time.sleep(0.5)
    
    try:
        data, addr = sock.recvfrom(1024)
        print(data, addr)
    except:
        print("time out")
        pass

#End