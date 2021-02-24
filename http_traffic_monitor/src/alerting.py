from time import localtime, strftime
import logging
import src.utils as utils

logger = utils.get_logger(__name__)


class AlertManager:
    """
    HTTP Packet sniffer and Collector class. Actively listens and filters for HTTP traffic, and adds to a collection
    separated into requests and responses.

    Attributes:
        alert_active (bool): Whether an alert is currently active or not.
        alert_threshold (float): The threshold which has to be crossed on average over a 2 minute span to trigger an alert.
        This is a float because otherwise with an int rounding down can lead to less tight alert checking.
        past_alerts (list<tuple(str, str)>): A list of tuples, each containing the string representation of the start
        and end time of past alerts.
        current_alert_start_time (str): the string representation of the start time of the current alert, if any.
    """
    def __init__(self, threshold):
        self.alert_active = False
        self.alert_threshold = float(threshold)
        self.past_alerts = []
        self.current_alert_start_time = ''
        self.alert_logfile = '/var/log/past_alerts.log'
        self.alert_logger = self.get_alert_logger()

    def get_alert_logger(self):
        """
        :return: (logger) A logger specifically for past alert logging.
        Logs all past alerts into a logfile. This allows for the console program to keep tidy and only show the last 5
        alerts, while still maintaining record of all past alerts.
        """
        logger = logging.getLogger('past_alerts')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(self.alert_logfile)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    def show_alerts(self):
        if self.alert_active:
            print(f'High traffic alert currently active! triggered at: {self.current_alert_start_time}.\n')
        else:
            print('No currently active alerts.\n')
        print(self.show_past_alerts())

    def show_past_alerts(self):
        """
        :return: (str) String of past alerts.
        Shows past alert start and end times. If there are more than 5, directs user to look at a logfile.
        """
        if not self.past_alerts:
            return 'No Past alerts to display.\n'
        past_alerts_str = 'Past Alerts:\n'
        if len(self.past_alerts) > 5:
            for alert_start_time, alert_end_time in self.past_alerts[::-1][:5]:
                past_alerts_str += f'\tPast alert started: {alert_start_time}, ended: {alert_end_time}.\n'
            past_alerts_str += 'Alerts printed limited to last 5 alerts. ' \
                               f'To find more past alerts see log file: {self.alert_logfile}\n'
        else:
            for alert_start_time, alert_end_time in self.past_alerts[::-1]:
                past_alerts_str += f'\tPast alert started: {alert_start_time}, ended: {alert_end_time}.\n'
        return past_alerts_str

    def determine_alert_state(self, average_hits):
        """
        :param average_hits: (float) The average hits in a 2 minute window
        :return: None
        If the average hits exceed the threshold and no alert is active, activate alert, save and print the start time.
        Otherwise if average hits is at or below the threshold, recover alert and save the time and print.
        """
        logger.debug(f'Checking average hits: {average_hits} against threshold: {self.alert_threshold}.'
                     f'Alert currently active: {self.alert_active}')
        if average_hits > self.alert_threshold and not self.alert_active:
            logger.info(f'Average above threshold and no alert active. Starting new alert.')
            self.alert_active = True
            self.current_alert_start_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
            print(f'High traffic generated an alert - hits = {round(average_hits, 2)},'
                  f' triggered at: {self.current_alert_start_time}')
        elif average_hits <= self.alert_threshold and self.alert_active:
            logger.info(f'Average below threshold and alert active. Clearing alert.')
            self.alert_active = False
            alert_recovered_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
            self.alert_logger.info(f'Past alert started: {self.current_alert_start_time}, ended: {alert_recovered_time}.\n')
            self.past_alerts.append(
                (self.current_alert_start_time, alert_recovered_time)
            )
            print(f'High traffic alert recovered at: {alert_recovered_time}')
