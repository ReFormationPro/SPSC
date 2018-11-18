import socket as Socket
import json as JSON

def getPacket(socket, header_length=1):
  if socket._closed:
    print("getPacket: socket closed")
  ## Get Packet Header
  #data_size = socket.recv(header_length)
  data_size = _recvFix(socket, header_length)
  ## Get Packet Content
  #data = socket.recv(int.from_bytes(data_size, byteorder="big"))
  data = _recvFix(socket, int.from_bytes(data_size, byteorder="big"))
  if data == b'':
    return {"type": "DEADBEEF"}
  return JSON.loads(data)

def sendPacket(socket, obj):
  if socket._closed:
    print("sendPacket: socket closed")
  data = JSON.dumps(obj)
  socket.sendall(bytes([len(data)])+bytes(data, "utf8"))   #send header

def _recvFix(conn, length):
  data = b''  # recv() does return bytes
  while True:
    try:
      chunk = conn.recv(length)  # some 2^n number
      if not chunk:  # chunk == ''
        break
      data += chunk
    except Socket.error:
      conn.close()
      break
    except OverflowError:
      print(length)
  return data
