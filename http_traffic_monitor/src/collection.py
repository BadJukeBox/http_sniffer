from scapy.sendrecv import AsyncSniffer
from scapy.layers import http
from scapy.layers.inet import TCP
from threading import Lock
import http_traffic_monitor.src.utils as utils

logger = utils.get_logger(__name__)


class HTTPPacketCollector:
    """
    HTTP Packet sniffer and Collector class. Actively listens and filters for HTTP traffic, and adds to a collection
    separated into requests and responses.

    Attributes:
        sniffer (scapy.sendrecv.AsyncSniffer): packet sniffer, set to filter on port 80, and turn filter out received
        packets that are not HTTP related. Can listen on one interface or all.
        collection (HTTPEventCollection): Collection of all HTTP filtered packets from the sniffer class.
        lock (threading.Lock): A lock so that when we clear the current collection of items, the sniffer can't try and
        accidentally add a packet that will get deleted before being processed by the statistics class.
    """
    def __init__(self):
        self.sniffer = None
        self.collection = HTTPEventCollection()
        self.lock = Lock()

    def start_packet_collection(self, interface=None):
        """
        :param interface: (str) The interface being listened on, None is default which will listen on all interfaces.
        :return: None
        Creates a sniffer and attempts to start it if one does not exist.
        """
        if not self.sniffer:
            logger.info(f'Starting packet listener with interface: {interface} listening for traffic on port 80.')
            self.sniffer = AsyncSniffer(iface=interface, prn=self.process_packet, filter="tcp port 80")
        if not self.sniffer.running:
            self.sniffer.start()

    def stop_packet_collection(self):
        """
        :return: None
        Stop the sniff.
        """
        if self.sniffer.running:
            logger.info(f'Stopping packet listener.')
            self.sniffer.stop()

    def process_packet(self, packet):
        """
        :param packet: ('scapy.layers.l2.Ether)
        :return: None
        Determines if a given packet is an HTTP request/response and if so, turns it into a data object and stores it.
        Locked so that if the collection is being remade it will not miss the datapoint accidentally.
        """
        self.lock.acquire()
        if packet.haslayer(http.HTTPRequest):
            self.collection.add_request_packet(HTTPRequestPacket(packet.Host, packet.Path, packet.Method, packet[TCP].ack))
        if packet.haslayer(http.HTTPResponse):
            self.collection.add_response_packet(HTTPResponsePacket(packet.Status_Code, packet[TCP].seq))
        self.lock.release()

    def clear_current_collection(self):
        """
        :return: None
        Clears the current HTTP request/response collection. Locked so that potential adding of packets does not occur
        during the process.
        """
        self.lock.acquire()
        logger.info('Clearing current HTTP packet collection data.')
        self.collection = HTTPEventCollection()
        self.lock.release()


class HTTPEventCollection:
    """
    Event Collection class.

    Attributes:
        http_request_list (list<HTTPRequestPacket>): The current list of HTTP requests in HTTPRequestPacket form.
        http_response_list (list<HTTPRequestPacket>): The current list of HTTP requests in HTTPResponsePacket form.
    """
    def __init__(self):
        self.http_request_list = []
        self.http_response_list = []

    def add_request_packet(self, packet):
        self.http_request_list.append(packet)

    def add_response_packet(self, packet):
        self.http_response_list.append(packet)


class HTTPRequestPacket:
    """
    Request Packet Data Object.

    Attributes:
        host (str): The host that was hit with no path included.
        path (str): The path hit for the given host.
        method (str): The request method used.
        ack_code (int): The ack code to link request to a given response.
    """
    def __init__(self, host, path, method, ack_code):
        self.host = str(host, 'UTF-8')
        self.path = str(path, 'UTF-8')
        self.method = str(method, 'UTF-8')
        self.ack_code = ack_code


class HTTPResponsePacket:
    """
    Request Packet Data Object.

    Attributes:
        status_code (int): The status of the call made in a request.
        seq_code (int): the seq code to link a response to a given request.
    """
    def __init__(self, status_code, seq_code):
        self.status_code = int(status_code)
        self.seq_code = seq_code
