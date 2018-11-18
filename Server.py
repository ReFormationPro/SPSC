import socket as Socket
import threading as Threading
from pprint import pprint
import Packet

def main():
  serverThread = startServer()
  #getCommands(serverThread)
  print("Goodbye.")

def getCommands(serverThread):
  print("Server Commands")
  while True:
    cmd = input("0- Halt")
    if cmd == "0":
      print("Halting the server.")
      serverThread.stop()
      break
    else:
      print("Unknown Command")

def startServer():
  thread = ServerThread()
  thread.start()
  return thread

class ServerThread(Threading.Thread):
  isRunning = True
  
  def __init__(self):
    super(ServerThread, self).__init__()

  def stop(self):
    self.isRunning = False

  def run(self):
    socket = Socket.socket()
    socket.bind(("localhost", 8888))
    socket.listen(99)
    while self.isRunning:
      clsocket, claddr = socket.accept()
      print(claddr)
      self._processClient(clsocket, claddr)
      clsocket.close()
    socket.close()

  def _processClient(self, sock, addr):
    #sock.send((b'A')*25)
    global latest
    latest = ClientHandlerThread(sock, addr)
    latest.start()

class ClientHandlerThread(Threading.Thread):
  isRunning = True
  PACKET_HEADER = 1

  def __init__(self, socket, addr):
    super(ClientHandlerThread, self).__init__()
    self.socket = socket
    self.addr = addr

  def stop(self):
    self.isRunning = False

  def run(self):
    while self.isRunning:
      Packet.sendPacket(self.socket, {"msg": "0- Close 1- Echo"})
      cmd = Packet.getPacket(self.socket, self.PACKET_HEADER)
      if cmd["type"] == "0":
        Packet.sendPacket(self.socket, {"msg": "Goodbye friend."})
        print("Closing the connection.")
        socket.close()
        self.stop()
        break
      elif cmd["type"] == "1":
        print("type 1 received")
        print(cmd["msg"])
        Packet.sendPacket(self.socket, {"msg": "haha I deceived you"})
      else:
        print("Unknown Command")

main()
