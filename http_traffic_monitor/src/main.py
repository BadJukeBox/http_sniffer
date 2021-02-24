from http_traffic_monitor.src.collection import HTTPPacketCollector
from http_traffic_monitor.src.statistics_management import StatisticsManager
from http_traffic_monitor.src.alerting import AlertManager
from argparse import ArgumentParser
from time import sleep
import http_traffic_monitor.src.utils as utils

logger = utils.get_logger(__name__)


def main(args):
    interval_count = 0
    statistics_check_interval_seconds = 10
    alert_check_interval = 12
    logger.info(f'Starting program and initializing packet collector.')
    logger.debug(f'Starting program with check interval: {statistics_check_interval_seconds} and alert interval:'
                 f'{alert_check_interval}.')
    packet_collector = HTTPPacketCollector()
    packet_collector.start_packet_collection(args.interface if args.interface else None)
    alerts = AlertManager(args.alert_trigger_threshold)
    statistics = StatisticsManager(alert_check_interval)

    statistics.show_all_statistics()

    while True:
        sleep(statistics_check_interval_seconds)
        interval_count += 1
        statistics.create_and_show_traffic_statistics(packet_collector.collection)
        packet_collector.clear_current_collection()
        if interval_count == alert_check_interval:
            logger.debug(f'Reached alert check interval of: {alert_check_interval}')
            alerts.determine_alert_state(statistics.average_hits_last_two_minutes)
            interval_count = 0
        alerts.show_alerts()


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-t', '--alert-trigger-threshold', required=True,
                            help='The threshold which will trigger an alert if crossed on average by traffic in a '
                                 'two minute window.')
    arg_parser.add_argument('-i', '--interface',
                            help='The interface to listen on. No input will automatically listen to all available '
                                 'interfaces.')
    main(arg_parser.parse_args())
