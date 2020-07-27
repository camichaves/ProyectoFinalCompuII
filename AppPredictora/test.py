import sys
from time import sleep
from filelock import FileLock

lock = FileLock("my_file.txt.lock")

with lock:
  open("my_file.txt","a").write("Hola desde el  proceso {}.".format(sys.argv[1]))
  sleep(2)
  print("Chau")
