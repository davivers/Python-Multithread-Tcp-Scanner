#!/usr/bin/env python3
from http import server
import socket
import ipaddress
import re
import threading
from queue import Queue

print_lock = threading.Lock()
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 1
port_max = 65535


print(r"""______            _     _  
|  _  \          (_)   | |
| | | |__ ___   ___  __| |
| | | / _` \ \ / / |/ _` |
| |/ / (_| |\ V /| | (_| |
|___/ \__,_| \_/ |_|\__,_|""")
print("\n****************************************************************")
print("\n* Copyright of David Lima, 2022                                *")
print("\n****************************************************************")


#Check if ip is avaiable for scan
while True:
    ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")
    try:
        ip_address_obj = ipaddress.ip_address(ip_add_entered)
        print("You entered a valid ip address.")
        break
    except:
        print("You entered an invalid ip address")
    
#check and format port input to minimize typing errors
while True:
    print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    port_range = input("Enter port range: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        port = port_min, port_max
        break

# Basic socket port scanning
def ports(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(0.5)
            s.connect((ip_add_entered, port))
            machine_host = socket.gethostbyaddr(ip_add_entered)[0]
            service = socket.getservbyport(port)
            with print_lock:
                print(f"Port {port} is open on: {ip_add_entered} | {machine_host} /| Service running: {service}")
            
        except:
            pass

#threading call
def threader():
    while True:
        worker = q.get()
        ports(worker)
        q.task_done()

q  = Queue()

for x in range(30):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(port_min, port_max + 1):
    q.put(worker)

q.join()