import os
import argparse
import configparser
from datetime import datetime, timedelta

from argo_archiver.NagiosResponse import NagiosResponse
from argo_archiver.utils import errmsg_from_excp


def parse_conf(file):
    config = configparser.ConfigParser()
    config.read(file)
    avro_file = '{}/{}'.format(config.get("Output", "Directory"), config.get("Output", "Filename"))
    logname = config.get("General", "LogName")
    return logname, avro_file


def inspect_file(consumer_name, avro_file):
    # Checks if files with today's stamp exist in all directories
    todays_date = datetime.today().strftime("%Y-%m-%d")
    todays_path = avro_file.replace('DATE', todays_date)
    status_track = dict(CRITICAL=list(), WARNING=list())

    import ipdb; ipdb.set_trace()

    try:
        stat_file = os.stat(avro_file)

    except FileNotFoundError:
        status_track['CRITICAL'].append(consumer_name)


    modify_time = datetime.fromtimestamp(todays_stats.st_mtime)
    time_two_hrs_ago = datetime.now() - timedelta(hours=2, minutes=0)

    # Checks if files have been modified in the last two hours
    if modify_time < time_two_hrs_ago:
        nagios.setCode(nagios.WARNING)
        nagios.writeWarningMessage(
            f"Today's file in {checked_conf.upper()} directory hasn't been modified in the last 2 hours.")



def main():
    parser = argparse.ArgumentParser(description="Sensor for checking freshness of avro files that ams-consumer produces")
    parser.add_argument('-f', dest='files', metavar='file', required=True, type=str, nargs='+',
                        help="Path of ams-consumer.conf files, wildcards allowed to match multiple files")

    cmd_options = parser.parse_args()

    for conf_file in cmd_options.files:
        consumer_name, avro_file = parse_conf(conf_file)
        status_file = inspect_file(consumer_name, avro_file)


if __name__ == "__main__":
    main()
