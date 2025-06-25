# argo-probe-archiver

Probe is inspecting `ams-consumer` component by checking the freshness of metric results data. Data is written on daily basis and stored in avro format. Correct path and filename of it is defined in configuration file `ams-consumer.conf`. Component can be spawn multiple times with the help of systemd instances and each has its own private configuration. Probe can check data of multiple instances by specifying their configuration files as arguments from which path and filename will be parsed, extracted and checked.

## Usage

Default arguments:
```
usage: archiver-probe [-h] -f file [file ...] -t hours

Sensor for checking freshness of avro files that ams-consumer produces

optional arguments:
  -h, --help          show this help message and exit
  -f file [file ...]  Path of ams-consumer.conf files, wildcards allowed to specify multiple files
  -t hours            Number of hours output file should not be older than
```
