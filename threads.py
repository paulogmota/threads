#!/usr/bin/python3

import socket
import os
import signal
import time
import threading
import sys
import subprocess
from queue import Queue
from datetime import datetime

def main():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports = []

    target = sys.argv[1]
    error = ("Input error")
    try:
        t_ip = socket.gethostbyname(target)
    except (UnboundLocalError, socket.gaierror):
        print("\nUsage: threads 1.1.1.1\n")
        sys.exit()

    def portscan(port):

       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
       try:
          portx = s.connect((t_ip, port))
          with print_lock:
              print(f"{t_ip}:{port}")
              discovered_ports.append(str(port))
              portx.close()

       except (ConnectionRefusedError, AttributeError, OSError):
          pass

    def threader():
       while True:
          worker = q.get()
          portscan(worker)
          q.task_done()
      
    q = Queue()
     
    #startTime = time.time()
     
    for x in range(500):
       t = threading.Thread(target = threader)
       t.daemon = True
       t.start()

    for worker in range(1, 65535):
       q.put(worker)

    q.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit()
