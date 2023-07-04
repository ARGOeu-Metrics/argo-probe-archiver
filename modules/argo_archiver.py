import os
import argparse
import configparser
from datetime import datetime, timedelta

from argo_probe_archiver.NagiosResponse import NagiosResponse


def process_files(hostname):
    nagios = NagiosResponse("Service works fine.")

    config = configparser.ConfigParser()
    config.read(f'/etc/argo-ams-consumer/ams-consumer-{hostname}.conf')

    try:
        directory = config.get("Output", "Directory")
    
        files = os.listdir(directory)

        sorted_file_paths = sorted(files, key=lambda file: datetime.strptime(
            file.split('_')[-1].split('.')[0], "%Y-%m-%d"))

        # Checks if a file with today's stamp exists in the directory
        todays_date = datetime.today().strftime("%Y-%m-%d")
        todays_path = f'argo-consumer_log_{todays_date}.avro'

        if todays_path in sorted_file_paths:
            todays_stats = os.stat(f"/var/lib/argo-ams-consumer/{hostname}/{todays_path}")

            modify_time = datetime.fromtimestamp(todays_stats.st_mtime)
            time_two_hrs_ago = datetime.now() - timedelta(hours=2, minutes=0)

            # Checks if the file has been modified in the last two hours
            if modify_time < time_two_hrs_ago:
                nagios.setCode(nagios.WARNING)
                nagios.writeWarningMessage("Today's file " + todays_path +
                    f" in {hostname.upper()} directory hasn't been modified in the last 2 hours.")

        else:
            nagios.setCode(nagios.CRITICAL)
            nagios.writeCriticalMessage(
                "Today's file " + todays_path + f" in {hostname.upper()} directory is missing for today.")

    except:
            nagios.setCode(nagios.CRITICAL)
            nagios.writeCriticalMessage("Directory does not exist.")

    print(nagios.getMsg())
    raise SystemExit(nagios.getCode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', dest='hostname',
                        required=True, type=str, help='SuperPOEM hostname')

    cmd_options = parser.parse_args()
    hostname = cmd_options.hostname

    process_files(hostname)

if __name__ == "__main__":
    main()
