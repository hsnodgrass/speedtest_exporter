#!/bin/env/python3

import subprocess
import json
import sys
from __future__ import print_function
from prometheus_client import Gauge, start_http_server

download_speed_gauge = Gauge('download_speed', 'Download speed in bits')
upload_speed_gauge = Gauge('upload_speed', 'Upload speed in bits')
latency_speed_gauge = Gauge('latency_speed', 'Internet Latency')

start_http_server(8001)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main():
    while True:
        s1 = subprocess.Popen(['speedtest-cli', '--json'], stdout=subprocess.PIPE, universal_newlines=True)
        s2 = s1.communicate()
        try:
            st_json = json.loads(s2[0])
        except JSONDecodeError as err:
            eprint("ERROR: Failed to parse JSON, setting all values to 0!")
            st_json['download'] = 0
            st_json['upload'] = 0
            st_json['ping'] = 0
        
        download_speed_gauge.set(st_json['download'])
        upload_speed_gauge.set(st_json['upload'])
        latency_speed_gauge.set(st_json['ping'])

if __name__ == "__main__":
    main()