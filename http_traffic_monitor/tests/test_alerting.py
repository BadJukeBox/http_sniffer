import unittest

from http_traffic_monitor.src.alerting import AlertManager


class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.alert_man = AlertManager(10)

    def test_show_past_alerts(self):
        assert self.alert_man.show_past_alerts() == 'No Past alerts to display.\n'
        self.alert_man.past_alerts = [
            ('Tue, 23 Feb 2021 04:04:08', 'Tue, 23 Feb 2021 04:06:08'),
            ('Tue, 23 Feb 2021 04:08:08', 'Tue, 23 Feb 2021 04:10:08')
        ]
        resp = self.alert_man.show_past_alerts()
        assert resp == 'Past Alerts:\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 04:08:08, ended: Tue, 23 Feb 2021 04:10:08.\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 04:04:08, ended: Tue, 23 Feb 2021 04:06:08.\n'

        self.alert_man.past_alerts = [
            ('Tue, 23 Feb 2021 04:04:08', 'Tue, 23 Feb 2021 04:06:08'),
            ('Tue, 23 Feb 2021 04:08:08', 'Tue, 23 Feb 2021 04:10:08'),
            ('Tue, 23 Feb 2021 06:04:08', 'Tue, 23 Feb 2021 06:06:08'),
            ('Tue, 23 Feb 2021 07:08:08', 'Tue, 23 Feb 2021 07:10:08'),
            ('Tue, 23 Feb 2021 08:04:08', 'Tue, 23 Feb 2021 08:06:08'),
            ('Tue, 23 Feb 2021 09:08:08', 'Tue, 23 Feb 2021 09:10:08')
        ]
        resp = self.alert_man.show_past_alerts()
        assert resp == 'Past Alerts:\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 09:08:08, ended: Tue, 23 Feb 2021 09:10:08.\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 08:04:08, ended: Tue, 23 Feb 2021 08:06:08.\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 07:08:08, ended: Tue, 23 Feb 2021 07:10:08.\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 06:04:08, ended: Tue, 23 Feb 2021 06:06:08.\n' \
                       '\tPast alert started: Tue, 23 Feb 2021 04:08:08, ended: Tue, 23 Feb 2021 04:10:08.\n' \
                       'Alerts printed limited to last 5 alerts. ' \
                       'To find more past alerts see log file: /var/log/past_alerts.log\n'

    def test_determine_alert_state(self):
        self.alert_man.determine_alert_state(10)
        assert not self.alert_man.alert_active
        assert self.alert_man.current_alert_start_time == ''
        assert self.alert_man.past_alerts == []

        self.alert_man.determine_alert_state(11)
        assert self.alert_man.alert_active
        assert self.alert_man.current_alert_start_time != ''
        assert self.alert_man.past_alerts == []

        self.alert_man.determine_alert_state(9)
        assert not self.alert_man.alert_active
        assert len(self.alert_man.past_alerts) == 1
