from http_traffic_monitor.src.collection import HTTPEventCollection, HTTPRequestPacket, HTTPResponsePacket
from scapy.layers.l2 import Ether

COLLECTION_DATA = HTTPEventCollection()
COLLECTION_DATA.http_request_list = [
    HTTPRequestPacket(b'google.com', b'/', b'GET', 123),
    HTTPRequestPacket(b'google.com', b'/somepath/', b'GET', 1232),
    HTTPRequestPacket(b'yahoo.com', b'/', b'GET', 1234),
    HTTPRequestPacket(b'drive.google.com', b'/drive/', b'GET', 1236)
]
COLLECTION_DATA.http_response_list = [
    HTTPResponsePacket(b'301', 123545),
    HTTPResponsePacket(b'301', 123543),
    HTTPResponsePacket(b'200', 123547),
    HTTPResponsePacket(b'400', 123546)
]
REQUEST_PACKET = Ether(b'\x02B!|\xe7\xb8\x02B\xac\x11\x00\x02\x08\x00E\x00\x00r\xe5\xe2@\x00@\x06\xd5\x87\xac\x11\x00\x02\x8e\xfaD\x0e\xb7P\x00P\xb0\x08E\x9c\x1a\xfe\xea\xfaP\x18\x01\xf6\x7f\x80\x00\x00GET / HTTP/1.1\r\nHost: google.com\r\nUser-Agent: curl/7.74.0\r\nAccept: */*\r\n\r\n')
RESPONSE_PACKET = Ether(b'\x02B\xac\x11\x00\x02\x02B!|\xe7\xb8\x08\x00E\x00\x028\xa6L\x00\x00%\x06nX\x8e\xfaD\x0e\xac\x11\x00\x02\x00P\xb7P\x1a\xfe\xea\xfa\xb0\x08E\xe6P\x18\xff\xff\x81\x8e\x00\x00HTTP/1.1 301 Moved Permanently\r\nLocation: http://www.google.com/\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Wed, 24 Feb 2021 02:21:05 GMT\r\nExpires: Fri, 26 Mar 2021 02:21:05 GMT\r\nCache-Control: public, max-age=2592000\r\nServer: gws\r\nContent-Length: 219\r\nX-XSS-Protection: 0\r\nX-Frame-Options: SAMEORIGIN\r\n\r\n<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">\n<TITLE>301 Moved</TITLE></HEAD><BODY>\n<H1>301 Moved</H1>\nThe document has moved\n<A HREF="http://www.google.com/">here</A>.\r\n</BODY></HTML>\r\n')
