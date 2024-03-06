import os
import argparse
import configparser
from datetime import datetime, timedelta

from argo_probe_archiver.NagiosResponse import NagiosResponse
from argo_probe_archiver.utils import errmsg_from_excp


def parse_conf(file):
    config = configparser.ConfigParser()
    config.read(file)
    avro_file = '{}/{}'.format(config.get("Output", "Directory"), config.get("Output", "Filename"))
    logname = config.get("General", "LogName")
    return logname, avro_file


def inspect_file(nagios, consumer_name, avro_file, hours):
    # Checks if files with today's stamp exist in all directories
    todays_date = datetime.today().strftime("%Y-%m-%d")
    avro_file = avro_file.replace('DATE', todays_date)
    status_track = dict(CRITICAL=list(), WARNING=list())

    try:
        stat_file = os.stat(avro_file)

    except FileNotFoundError:
        status_track['CRITICAL'].append(consumer_name)

    modify_time = datetime.fromtimestamp(stat_file.st_mtime)
    time_two_hrs_ago = datetime.now() - timedelta(hours=hours, minutes=0)

    # Checks if files have been modified in the last two hours
    if modify_time < time_two_hrs_ago:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(
            f"Output file in {os.path.dirname(avro_file)} hasn't been modified in the last {hours} hours."
        )


def main():
    parser = argparse.ArgumentParser(description="Sensor for checking freshness of avro files that ams-consumer produces")
    parser.add_argument('-f', dest='files', metavar='file', required=True, type=str, nargs='+',
                        help="Path of ams-consumer.conf files, wildcards allowed to specify multiple files")
    parser.add_argument('-t', dest='hours', metavar='hours', required=True, type=int,
                        help="Number of hours output file should not be older than")

    cmd_options = parser.parse_args()

    nagios = NagiosResponse("All ams-consumers are fine")

    for conf_file in cmd_options.files:
        consumer_name, avro_file = parse_conf(conf_file)
        status_file = inspect_file(nagios, consumer_name, avro_file, cmd_options.hours)

    print(nagios.getMsg())
    raise SystemExit(nagios.getCode())


if __name__ == "__main__":
    main()
