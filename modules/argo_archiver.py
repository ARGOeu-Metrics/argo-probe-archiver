import os
import argparse
import configparser
from datetime import datetime, timedelta

from argo_probe_archiver.NagiosResponse import NagiosResponse
from argo_probe_archiver.utils import errmsg_from_excp


def parse_conffiles(arguments, file):
    config = configparser.ConfigParser()
    config.read(f"{arguments.path}/{file}")
    directory = config.get("Output", "Directory")
    return directory

def process_files(arguments):
    nagios = NagiosResponse("All services work fine.")
    try:
        for file in os.listdir(arguments.path):
            directory = parse_conffiles(arguments, file)

            files = os.listdir(directory)
            sorted_file_paths = sorted(files, key=lambda x: datetime.strptime(
                x.split('_')[-1].split('.')[0], "%Y-%m-%d"))

            # Checks if files with today's stamp exist in all directories
            todays_date = datetime.today().strftime("%Y-%m-%d")
            todays_path = f'argo-consumer_log_{todays_date}.avro'

            checked_conf = directory.split("/")[-1]

            if todays_path in sorted_file_paths:
                todays_stats = os.stat(f"{directory}/{todays_path}")

                modify_time = datetime.fromtimestamp(todays_stats.st_mtime)
                time_two_hrs_ago = datetime.now() - timedelta(hours=0, minutes=1)

                # Checks if files have been modified in the last two hours
                if modify_time < time_two_hrs_ago:
                    nagios.setCode(nagios.WARNING)
                    nagios.writeWarningMessage(
                        f"Today's file in {checked_conf.upper()} directory hasn't been modified in the last 2 hours.")

            else:
                nagios.setCode(nagios.CRITICAL)
                nagios.writeCriticalMessage(
                    f"Today's file in {checked_conf.upper()} directory is missing for today.")

    except FileNotFoundError:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"Directory does not exist.")

    except OSError as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")

    except ValueError as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")

    except Exception as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")

    print(nagios.getMsg())
    raise SystemExit(nagios.getCode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path', required=False,
                        type=str, default="/etc/argo-ams-consumer/")

    cmd_options = parser.parse_args()

    process_files(cmd_options)


if __name__ == "__main__":
    main()
