# argo-probe-archiver

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
