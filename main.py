# pysniff v1

import socket
import time

logo = r'''
                       _ ______
   ___  __ _____ ___  (_) _/ _/
  / _ \/ // (_-</ _ \/ / _/ _/ 
 / .__/\_, /___/_//_/_/_//_/   
/_/   /___/                    

https://github.com/0x18F

'''

def sniff():
        print(logo)
        time.sleep(2)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            HOST_IP = s.getsockname()[0]

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) as s:
            s.bind((HOST_IP, 0))
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            print("[+] Listening for traffic...")
            try:
                while True:
                    packet, addr = s.recvfrom(65565)
                    print(f'[+] Packet from {addr[0]} | Size: {len(packet)} bytes')
        
            except KeyboardInterrupt:
                s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                print('[-] Program ended by user')
    
if __name__ == "__main__":
    sniff()
            