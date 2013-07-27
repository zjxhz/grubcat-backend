#!/usr/bin/env python

import ssl
import json
import socket
import struct
import binascii
from datetime import datetime
# Send a notification
token = '691dabb1da8d277ab05a7d7a13a94b178925d821caa87a116facd883f0c9ec88' #'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
payload = {
    'aps': {
        'alert': 'Hello Push! %s ' % datetime.now(),
    }
}

def push(token, payload):
    # the certificate file generated from Provisioning Portal
    certfile = '/home/fanju/src/grubcat-backend/apns_combine.pem'

    #APNS server address (use 'gateway.push.apple.com' for production server)
    apns_address = ('gateway.push.apple.com', 2195)

    # create socket and connect to APNS server using SSL
    s = socket.socket()
    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=certfile)
    sock.connect(apns_address)

    # generate APNS notification packet
    token = binascii.unhexlify(token)
    fmt = "!ciiH32sH{0:d}s".format(len(payload))
    cmd = '\x01'
    msg = struct.pack(fmt, cmd, 0, 0, len(token), token, len(payload), payload)
    print "binary message: %s" % msg
    sock.write(msg)
    # sock.setblocking(0)
    # try:
    #    feedback = sock.recv(128)
    #    print "feedback: %s" % feedback
    # except Exception as e:
    #    print "no feedback: %s" % e
    sock.close()

if __name__ == '__main__':
    push(token, json.dumps(payload))