from collection import HTTPPacketCollector
from statistics_management import StatisticsManager
from alerting import AlertManager
from argparse import ArgumentParser
from time import sleep


def main(args):
    alert_timer = 0  # every 12 10 second waits we'll also check for the 2m mark
    packet_collector = HTTPPacketCollector()
    packet_collector.start_packet_collection(args.interface if args.interface else None)
    alerts = AlertManager(int(args.alert_trigger_threshold))
    statistics = StatisticsManager()
    statistics.show_all_statistics()
    while True:
        sleep(10)
        alert_timer += 1
        statistics.calculate_statistics(packet_collector.collection)
        statistics.show_all_statistics()
        statistics.clear_recent_statistics()
        packet_collector.clear_current_collection()
        if alert_timer == 1:
            alerts.determine_alert_state(statistics.average_hits_last_two_minutes)
            alert_timer = 0
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
