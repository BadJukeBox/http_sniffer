import unittest

from http_traffic_monitor.src.statistics_management import StatisticsManager
from http_traffic_monitor.tests.test_data import event_collection_data


class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.statistics = StatisticsManager(10)

    def test_calculate_two_minute_average(self):
        for i in range(0, 9):
            self.statistics.calculate_two_minute_average(10)
            assert self.statistics.average_hits_last_two_minutes == 0
            assert len(self.statistics.hits_last_two_minutes) == i+1

        self.statistics.calculate_two_minute_average(10)
        assert self.statistics.average_hits_last_two_minutes == 10.0
        assert not self.statistics.hits_last_two_minutes

    def test_accumulate_request_statistics(self):
        self.statistics.accumulate_request_statistics(event_collection_data.COLLECTION_DATA.http_request_list)
        assert len(self.statistics.sites_recent.keys()) == 3
        assert self.statistics.total_method_counts['GET'] == 4
        assert self.statistics.total_calls_count == 4

        assert self.statistics.sites_recent['google.com']['sections'] == ['/', '/somepath']
        assert self.statistics.sites_recent['google.com']['site_hit_count'] == 2
        assert self.statistics.sites_recent['yahoo.com']['sections'] == ['/']
        assert self.statistics.sites_recent['yahoo.com']['site_hit_count'] == 1
        assert self.statistics.sites_recent['drive.google.com']['sections'] == ['/drive']
        assert self.statistics.sites_recent['drive.google.com']['site_hit_count'] == 1

    def test_accumulate_response_statistics(self):
        self.statistics.accumulate_response_statistics(event_collection_data.COLLECTION_DATA.http_response_list)
        assert self.statistics.total_failures_count == 1
        assert self.statistics.total_successes_count == 3

    def test_calculate_statistics(self):
        self.statistics.calculate_statistics(event_collection_data.COLLECTION_DATA)
        assert len(self.statistics.sites_total) == 3
        for site in self.statistics.sites_recent:
            assert self.statistics.sites_total[site] == self.statistics.sites_recent[site]['site_hit_count']

        self.statistics.sites_recent = {}
        self.statistics.calculate_statistics(event_collection_data.COLLECTION_DATA)
        assert len(self.statistics.sites_total) == 3
        print(self.statistics.sites_recent)
        print(self.statistics.sites_total)
        for site in self.statistics.sites_recent:
            assert self.statistics.sites_total[site] == 2*(self.statistics.sites_recent[site]['site_hit_count'])

    def test_generate_most_visited_site_stats_display(self):
        assert self.statistics.generate_most_visited_site_stats_display() == 'No sites visited in the last 10 seconds.\n'

        self.statistics.calculate_statistics(event_collection_data.COLLECTION_DATA)
        resp = self.statistics.generate_most_visited_site_stats_display()
        assert resp == 'Most visited site in the last 10 seconds: google.com.\n' \
                       'google.com sections hit: \n' \
                       '\t/\n' \
                       '\t/somepath\n'

    def test_generate_total_stats_display(self):
        self.statistics.total_calls_count = 5
        self.statistics.total_failures_count = 3
        self.statistics.total_successes_count = 2

        resp = self.statistics.generate_total_stats_display()
        assert resp == 'Total Statistics:\n\tTotal Requests: 5\n\t' \
               'Total Failures: 3\n\t' \
               'Total Successes: 2\n\n'

    def test_generate_totals_by_method_display(self):
        assert self.statistics.generate_totals_by_method_display() == 'No Requests made yet.'

        self.statistics.total_method_counts = {'GET': 10, 'POST': 10}
        resp = self.statistics.generate_totals_by_method_display()
        assert resp == 'Total Counts by Request Method:\n' \
                       '\tMethod: GET - Count: 10\n' \
                       '\tMethod: POST - Count: 10\n'

    def test_generate_top_sites_display(self):
        assert self.statistics.generate_top_sites_display() == 'No sites visited yet.'
        self.statistics.sites_total = {'mysite.com': 10, 'mysite2.com': 1}
        resp = self.statistics.generate_top_sites_display()
        assert resp == 'Top 2 Site totals:\n' \
                       '\tSite: mysite.com - Hits: 10\n' \
                       '\tSite: mysite2.com - Hits: 1\n'

        self.statistics.sites_total = {'mysite.com': 10, 'mysite2.com': 8, 'mysite3.com': 3, 'mysite4.com': 5,
                                       'mysite5.com': 2, 'mysite6.com': 1}
        resp = self.statistics.generate_top_sites_display()
        assert resp == 'Top 5 Site totals:\n' \
                       '\tSite: mysite.com - Hits: 10\n' \
                       '\tSite: mysite2.com - Hits: 8\n' \
                       '\tSite: mysite4.com - Hits: 5\n' \
                       '\tSite: mysite3.com - Hits: 3\n' \
                       '\tSite: mysite5.com - Hits: 2\n'
