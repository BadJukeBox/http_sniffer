# import unittest
#
# from http_traffic_monitor.src.collection import HTTPPacketCollector
# from http_traffic_monitor.tests.test_data import event_collection_data
#
#
# class TestHTTPPacketCollector(unittest.TestCase):
#     def setUp(self):
#         self.http_collector = HTTPPacketCollector()
#
#     def test_start_packet_collection(self):
#
#         assert not self.http_collector.sniffer
#
#         self.http_collector.start_packet_collection()
#         assert self.http_collector.sniffer
#         assert self.http_collector.sniffer.running
#
#     def test_stop_packet_collection(self):
#         self.http_collector.start_packet_collection()
#
#         assert self.http_collector.sniffer.running
#         self.http_collector.stop_packet_collection()
#
#         assert self.http_collector.sniffer
#         assert not self.http_collector.sniffer.running
#
#     def test_process_packet(self):
#         self.http_collector.process_packet(event_collection_data.REQUEST_PACKET)
#         assert len(self.http_collector.collection.http_request_list) == 1
#         assert len(self.http_collector.collection.http_response_list) == 0
#
#         self.http_collector.process_packet(event_collection_data.RESPONSE_PACKET)
#         assert len(self.http_collector.collection.http_request_list) == 1
#         assert len(self.http_collector.collection.http_response_list) == 1
#
#     def test_clear_current_collection(self):
#         self.http_collector.process_packet(event_collection_data.REQUEST_PACKET)
#         assert self.http_collector.collection.http_request_list
#
#         self.http_collector.clear_current_collection()
#
#         assert not self.http_collector.collection.http_request_list
#         assert not self.http_collector.collection.http_response_list
