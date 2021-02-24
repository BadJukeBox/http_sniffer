from http_traffic_monitor.src.collection import HTTPEventCollection, HTTPRequestPacket, HTTPResponsePacket

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

REQUEST_PACKET = b''
RESPONSE_PACKET = b''
