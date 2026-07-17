# pysniff v1

import socket

def sniff():
   
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
                    print(f'Packet from {addr[0]} | Size: {len(packet)} bytes')
        
            except KeyboardInterrupt:
                print('[-] Program ended')
                s.ioctl(socket.RCVALL_OFF)
    
if __name__ == "__main__":
    sniff()
            