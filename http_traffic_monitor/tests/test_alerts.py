from http_traffic_monitor.src.collection import HTTPPacketCollector
from http_traffic_monitor.src.statistics_management import StatisticsManager
from http_traffic_monitor.src.alerting import AlertManager
import requests
import unittest


class TestAlert(unittest.TestCase):
    def setUp(self):
        self.packet_collector = HTTPPacketCollector()

    def test_alerts_with_traffic(self):
        self.packet_collector.start_packet_collection()
        alerts = AlertManager(5)
        statistics = StatisticsManager(1)

        for i in range(6):
            requests.get('http://www.google.com')

        statistics.create_and_show_traffic_statistics(self.packet_collector.collection)
        self.packet_collector.clear_current_collection()

        alerts.determine_alert_state(statistics.average_hits_last_two_minutes)
        assert alerts.alert_active

        for i in range(6):
            requests.get('http://www.datadoghq.com')

        statistics.create_and_show_traffic_statistics(self.packet_collector.collection)
        self.packet_collector.clear_current_collection()

        alerts.determine_alert_state(statistics.average_hits_last_two_minutes)
        assert alerts.alert_active

        statistics.create_and_show_traffic_statistics(self.packet_collector.collection)
        self.packet_collector.clear_current_collection()

        alerts.determine_alert_state(statistics.average_hits_last_two_minutes)
        assert not alerts.alert_active
