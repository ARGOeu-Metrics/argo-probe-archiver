import os
import argparse
import configparser
from datetime import datetime, timedelta

from argo_probe_archiver.NagiosResponse import NagiosResponse
from argo_probe_archiver.utils import errmsg_from_excp

def process_files(path):
    nagios = NagiosResponse("All services works fine.")

    try:
        for file in os.listdir(path):
            config = configparser.ConfigParser()
            config.read(f"{path}/{file}")
            
            directory = config.get("Output", "Directory")        
            files = os.listdir(directory)   
        
            sorted_file_paths = sorted(files, key=lambda file: datetime.strptime(
                    file.split('_')[-1].split('.')[0], "%Y-%m-%d"))
        
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
                    nagios.writeWarningMessage(f"Today's file in {checked_conf.upper()} directory hasn't been modified in the last 2 hours.")
                            
            else:
                nagios.setCode(nagios.CRITICAL)
                nagios.writeCriticalMessage(
                    f"Today's file in {checked_conf.upper()} directory is missing for today.")
    
    except ValueError as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")

    except OSError as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")

    except Exception as e:
        nagios.setCode(nagios.CRITICAL)
        nagios.writeCriticalMessage(f"{errmsg_from_excp(e)}")
    
    print(nagios.getMsg())
    raise SystemExit(nagios.getCode())
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path', required=True, type=str)

    cmd_options = parser.parse_args()
    path = cmd_options.path

    process_files(path)

if __name__ == "__main__":
    main()
