#!/bin/env/python3
from __future__ import print_function
import subprocess
import json
import sys
from prometheus_client import Gauge, start_http_server

download_speed_gauge = Gauge('speed_measured', 'The metric speed being exported.')
upload_speed_gauge = Gauge('speed_measured', 'The metric speed being exported.')
latency_speed_gauge = Gauge('speed_measured', 'The metric speed being exported.')

start_http_server(8000)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main():
    while True:
        s1 = subprocess.Popen(['speedtest-cli', '--json'], stdout=subprocess.PIPE, universal_newlines=True)
        s2 = s1.communicate()
        try:
            st_json = json.loads(s2[0])
        except json.decoder.JSONDecodeError:
            eprint("ERROR: Failed to parse JSON, setting all values to 0!")
            st_json = {'download': 0, 'upload': 0, 'ping': 0}

        download_speed_gauge.labels(speed_measured='download').set(st_json['download'])
        upload_speed_gauge.labels(speed_measured='upload').set(st_json['upload'])
        latency_speed_gauge.labels(speed_measured='latency').set(st_json['ping'])

if __name__ == "__main__":
    main()
    