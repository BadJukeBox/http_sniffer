from os import system


class StatisticsManager:
    """
    A Statistics computation/accumulation class. contains methods both to calculate statistics, and to display them.

    Attributes:
        total_calls_count (int): The total requests recorded during the lifetime of the program.
        total_failures_count (int): The total requests failures recorded during the lifetime of the program.
        total_successes_count (int): The total requests successes recorded during the lifetime of the program.
        total_method_counts (dict): The total number of calls recorded during the lifetime of the program broken down
        by the request method. IE: {'GET': 10, 'POST': 10}
        hits_last_two_minutes (list<int>): Holds the last 12 10 second sequences in order to calculate the average hits for
        the past 2 minutes. Each time a new 10 second window is added, the first is removed, in a queue fashion.
        sites_recent (dict): A representation of the current set of requests, recording a host, it's hits, and the
        sections that were hit. IE: {'mysite.com': {'site_hit_count': 10, 'sections': ['/section1', '/section2', ',']}}
        sites_total (dict): A representation of the sites hit  during the lifetime of the program, and their hit counts.
        IE: {'mysite.com': 10, 'mysite2.com': 1}
    """
    def __init__(self):
        self.total_calls_count = 0
        self.total_failures_count = 0
        self.total_successes_count = 0
        self.total_method_counts = {}

        self.hits_last_two_minutes = []
        self.average_hits_last_two_minutes = 0

        self.sites_recent = {}
        self.sites_total = {}

    def calculate_statistics(self, collection):
        """
        :param collection: (HTTPEventCollection) Collection of HTTP events sniffed in the past 10 second window.
        :return: None
        Accumulates statistics from the past 10 second window and adds them to running total statistics.
        """
        self.accumulate_request_statistics(collection.http_request_list)
        self.accumulate_response_statistics(collection.http_response_list)

        recent_sites_total_hits = 0
        for site in self.sites_recent:
            if site not in self.sites_total:
                self.sites_total[site] = self.sites_recent[site]['site_hit_count']
            else:
                self.sites_total[site] += self.sites_recent[site]['site_hit_count']
            recent_sites_total_hits += self.sites_recent[site]['site_hit_count']

        self.calculate_two_minute_average(recent_sites_total_hits)

    def calculate_two_minute_average(self, recent_hits_total):
        """
        :param recent_hits_total: (int) the total hits for the most recent 10 second window.
        Add recent hits total, and if we have hit our threshold for calculating average, calculate and clear the list.
        """
        self.hits_last_two_minutes.append(recent_hits_total)
        print(self.hits_last_two_minutes)
        if len(self.hits_last_two_minutes) >= 1:
            self.average_hits_last_two_minutes = int(sum(self.hits_last_two_minutes)/len(self.hits_last_two_minutes))
            self.hits_last_two_minutes = []

    def show_all_statistics(self):
        """
        :return: None
        generates and prints statistics information for both recent and running totals.
        """
        system('clear')
        print(self.generate_most_visited_site_stats_display())
        print(self.generate_total_stats_display())
        print(self.generate_totals_by_method_display())
        print(self.generate_top_sites_display())

    def clear_recent_statistics(self):
        """
        :return: None
        Clears the most recent site data. This ensures that every 10 seconds the data is fresh.
        """
        self.sites_recent = {}

    def accumulate_request_statistics(self, http_request_list):
        """
        :param http_request_list: (list<HTTPRequestPacket>) the request packets gathered in the last 10 seconds.
        :return: None
        Checks the request path, and separates it into only the initial section (the first piece of the bath before the
        second '/' ie: site.com/section/2/ section = /section. The section is then added to a list for each host if not
        already visited. Site hit/total call counters are then updated.
        """
        for request in http_request_list:
            if request.path == '/':
                section = request.path
            else:
                section = '/'.join(request.path.split('/')[:2])
            if request.host not in self.sites_recent:
                self.sites_recent[request.host] = {
                    'sections': [section],
                    'site_hit_count': 1
                }
            else:
                if section not in self.sites_recent[request.host]['sections']:
                    self.sites_recent[request.host]['sections'].append(section)
                self.sites_recent[request.host]['site_hit_count'] += 1

            self.total_method_counts[request.method] = self.total_method_counts.get(request.method, 0) + 1
            self.total_calls_count += 1

    def accumulate_response_statistics(self, http_response_list):
        """
        :param http_response_list: (list<HTTPResponsePacket>) the response packets gathered in the last 10 seconds.
        :return: None
        Checks for bad response codes (simply >=400) and decides whether the response indicated a successful call.
        """
        for request in http_response_list:
            if request.status_code >= 400:
                self.total_failures_count += 1
            else:
                self.total_successes_count += 1

    def generate_most_visited_site_stats_display(self):
        """
        :return: (str) The message to display
        Displays the site with the most hits in the most recent 10 second window.
        Displays the different sections hit on said site during the same window.
        """
        if not self.sites_recent:
            return 'No sites visited in the last 10 seconds.\n'

        most_visited_site = sorted(self.sites_recent, key=lambda site: self.sites_recent[site]['site_hit_count'], reverse=True)[0]
        recent_sites_str = f'Most visited site in the last 10 seconds: {most_visited_site}.\n' \
                           f'{most_visited_site} sections hit: \n'
        for section in self.sites_recent[most_visited_site]['sections']:
            recent_sites_str += f'\t{section}\n'

        return recent_sites_str

    def generate_total_stats_display(self):
        """
        :return: (str) The message to display
        Displays overall totals for both calls that succeeded and failed.
        A difference in this number could indicate timeouts.
        """
        return f'Total Statistics:\n\tTotal Requests: {self.total_calls_count}\n\t' \
               f'Total Failures: {self.total_failures_count}\n\t' \
               f'Total Successes: {self.total_successes_count}\n\n'

    def generate_totals_by_method_display(self):
        """
        :return: (str) The message to display
        Display the total amount of requests made broken down by HTTP method.
        """
        if not self.total_method_counts:
            return 'No Requests made yet.'

        method_totals_str = f'Total Counts by Request Method:\n'
        for method in self.total_method_counts:
            method_totals_str += f'\tMethod: {method} - Count: {self.total_method_counts[method]}\n'

        return method_totals_str

    def generate_top_sites_display(self, top_n=5):
        """
        :param top_n: (int) The number of top hit sites to display. 5 by default.
        :return: (str) The message to display
        Displays either the number of top sites specified and their hits,
        or if there are less than specified, that amount.
        """
        if not self.sites_total:
            return 'No sites visited yet.'

        descending_top_sites = sorted(self.sites_total.items(), key=lambda site_total: site_total[1], reverse=True)

        if len(self.sites_total) < top_n:
            descending_top_sites = dict(descending_top_sites)
        else:
            descending_top_sites = dict(descending_top_sites[:top_n])

        top_sites_str = f'Top {len(descending_top_sites)} Site totals:\n'
        for site in descending_top_sites:
            top_sites_str += f'\tSite: {site} - Hits: {descending_top_sites[site]}\n'

        return top_sites_str
