#!/bin/env/python3
from __future__ import print_function
import subprocess
import json
import sys
from prometheus_client import Gauge, start_http_server

download_speed_gauge = Gauge('download_speed', 'Download speed.')
upload_speed_gauge = Gauge('upload_speed', 'Upload speed.')
latency_speed_gauge = Gauge('latency_speed', 'Network latency.')

start_http_server(8000)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    while True:
        try:
            print('Running speedtest-cli subprocess.')
            s1 = subprocess.Popen(['speedtest-cli', '--json'], stdout=subprocess.PIPE, universal_newlines=True)
            print('Communicating with subprocess.')
            s2 = s1.communicate()
            try:
                print('Loading speedtest into JSON variable.')
                st_json = json.loads(s2[0])
            except json.decoder.JSONDecodeError:
                print('ERROR: Failed to parse JSON, setting all values to 0')
                eprint("ERROR: Failed to parse JSON, setting all values to 0!")
                st_json = {'download': 0, 'upload': 0, 'ping': 0}
        except TypeError:
            print("Couldn't get results from speedtest-cli!")

        print('Setting gauge values.')
        download_speed_gauge.set(st_json['download'])
        upload_speed_gauge.set(st_json['upload'])
        latency_speed_gauge.set(st_json['ping'])

if __name__ == "__main__":
    main()
