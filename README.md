# pysniff v1.0

Network packet sniffer made in python, designed for Windows environments using raw sockets. This tool detects the active network interface and puts the network card into **promiscuous mode** via Windows IOCTL APIs to intercept incoming and outgoing IPv4 traffic.

> **Warning:** This tools interacts directly with the network layer via raw sockets so it requires Admin privilieges to run.

## Installation & Usage
1. Clone this repo:
```bash
   git clone https://github.com/0x18F/pysniff.git
   cd pysniff```
2. Open a terminal as admin & run the script:
```bash
python main.py```

To stop capturing and restore your network adapter settings, press Ctrl + C

