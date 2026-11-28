#!/usr/bin/env python3
# ssh ProxyCommand via the box's userspace tailscaled SOCKS5 (localhost:1055)
import socket,sys,struct,select,os
s=socket.create_connection(('127.0.0.1',1055))
s.sendall(b'\x05\x01\x00'); s.recv(2)
h=sys.argv[1].encode()
s.sendall(b'\x05\x01\x00\x03'+bytes([len(h)])+h+struct.pack('>H',int(sys.argv[2])))
r=s.recv(10)
if len(r)<2 or r[1]!=0: sys.exit("socks connect failed")
while True:
    a,_,_=select.select([s,0],[],[])
    if s in a:
        d=s.recv(65536)
        if not d: break
        os.write(1,d)
    if 0 in a:
        d=os.read(0,65536)
        if not d: s.shutdown(socket.SHUT_WR); continue
        s.sendall(d)
