#import the necessary socket, time for performance, threading for efficiency,
#sys for writing to a file, and datetime to acquire the realworld date and time
import socket
import time
import threading
import sys
import datetime

#the from queue import queue is necessary for threading
#entered a timeout time and a print lock which prevents a thread from using a
#variable that another thread is using
from queue import Queue
socket.setdefaulttimeout(0.5)
print_lock = threading.Lock()
now = datetime.datetime.now()

#IP address entering and acquiring the host
target = input('Type your IP address: ')
t_IP = socket.gethostbyname(target)
print('Scan in progress: ', t_IP)
print('Results Report', file=open('Port Scan Results.txt','a'))

#portscan function to connect to ports and print an open port to a file
def portscan(port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      con = s.connect((t_IP, port))
      with print_lock:
         print(port, 'open', file=open('Port Scan Results.txt','a'))
      con.close()
   except:
      pass

#function to ensure the task continues and is ended
def threader():
   while True:
      worker = q.get()
      portscan(worker)
      q.task_done()

#defining how the time taken is gathered
q = Queue()
startTime = time.time()

#loop for the defined range of ports
for x in range(70000):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()

#the ports scanned
for worker in range(1, 70001):
   q.put(worker)

#final results printed to file
q.join()
print('Time in seconds:', time.time() - startTime, file=open('Port Scan Results.txt','a'))
print(now.strftime("Date completed: %Y-%m-%d %H:%M:%S"), file=open('Port Scan Results.txt','a'))
