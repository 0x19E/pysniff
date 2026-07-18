# pysniff v1

import socket
import time
import subprocess
from rich import print

logo = r'''[white]
                       _ ______
   ___  __ _____ ___  (_) _/ _/
  / _ \/ // (_-</ _ \/ / _/ _/ 
 / .__/\_, /___/_//_/_/_//_/   
/_/   /___/                    

[red]https://github.com/0x18F[/red]

[/white]'''


subprocess.run('cls', shell=True)

def sniff():
        print(logo)
        time.sleep(2)

        # Get private IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            HOST_IP = s.getsockname()[0]

        #Enable promiscuous mode to see all packets
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) as s:
            s.bind((HOST_IP, 0))
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            print("[green][+] Listening for traffic...[/green]")

            # Filter packets by type
            try:
                while True:
                    packet, _ = s.recvfrom(65565)
                    protocol = packet[9]

                    src_ip_raw = packet[12:16]
                    dst_ip_raw = packet[16:20]

                    src_ip = socket.inet_ntoa(src_ip_raw)
                    dst_ip = socket.inet_ntoa(dst_ip_raw)

                    if protocol == 1:
                        print(f'[[yellow]+[/yellow]] [yellow]Ping | {src_ip} -> {dst_ip} | Size: {len(packet)} bytes[/yellow]')
                    elif protocol == 6:
                         print(f'[[green]+[/green]] [green]TCP | {src_ip} -> {dst_ip} | Size: {len(packet)} bytes[/green]')
                    elif protocol == 17:
                         print(f'[[bold blue]+[/bold blue]] [bold blue]UDP | {src_ip} -> {dst_ip} | Size: {len(packet)} bytes[/bold blue]')
                    else:
                        print(f'[[bold red]+[/bold red]] [bold red]Undefined | {src_ip} -> {dst_ip} | Size: {len(packet)} bytes[/bold red]')
        
            except KeyboardInterrupt:
                s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                print('[[red]-[/red]] Program ended by user')

            except Exception as e:
                 s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                 print(f"[[red]-[/red]] Error: {e}")

if __name__ == "__main__":
    sniff()
            