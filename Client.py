import socket as Socket
import json as JSON
import Packet

PACKET_HEADER = 1

def getCommands(socket):
  print("Client Commands")
  while True:
    cmd = input("What's your command?")
    if cmd == "0":
      print("Goodbye master.")
      Packet.sendPacket(socket, {"type": 0, "msg": "Muhahaha!"})
      return
    elif cmd == "1":
      print("1111111!!!!")
      Packet.sendPacket(socket, {"type": 0, "msg": "Muhahaha!"})
    else:
      print("Unknown Command")

def main():
  socket = Socket.socket()
  socket.connect(("localhost", 8888))
  data = Packet.getPacket(socket, PACKET_HEADER)
  print(data["msg"])  #print welcome message
  getCommands(socket)
  #socket.close()

main()

## BACKUP
def getPacket(socket, header_length):
  #Get Packet Header
  data_size = socket.recv(header_length)
  #Get Packet Content
  data = socket.recv(int.from_bytes(data_size, byteorder="big")).decode("utf-8")
  return JSON.loads(data)

def sendPacket(socket, obj):
  data = JSON.dumps(obj)
  socket.sendall(bytes([len(data)])+bytes(data, "utf8"))   #send header
  #socket.send(bytes(data, "utf8"))  #send packet content
