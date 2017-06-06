#!/bin/env/python3

import subprocess
import json
from prometheus_client import Gauge, start_http_server

download_speed_gauge = Gauge('download_speed', 'Download speed in bits')
upload_speed_gauge = Gauge('upload_speed', 'Upload speed in bits')
latency_speed_gauge = Gauge('latency_speed', 'Internet Latency')

start_http_server(8001)

def main():
    while True:
        s1 = subprocess.Popen(['speedtest-cli', '--json'], stdout=subprocess.PIPE, universal_newlines=True)
        s2 = s1.communicate()
        st_json = json.loads(s2[0])
        download_speed_gauge.set(st_json['download'])
        upload_speed_gauge.set(st_json['upload'])
        latency_speed_gauge.set(st_json['ping'])

if __name__ == "__main__":
    main()