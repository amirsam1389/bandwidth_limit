#!/usr/bin/env python3

import argparse
import subprocess

# ANSI escape code for yellow and blue colors
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'


def limit_bandwidth(interface, upload_limit, download_limit):
    subprocess.run(['tc', 'qdisc', 'del', 'dev', interface, 'root'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'root', 'handle', '1:', 'htb', 'default', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'class', 'add', 'dev', interface, 'parent', '1:', 'classid', '1:10', 'htb', 'rate', download_limit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'parent', '1:10', 'handle', '10:', 'sfq', 'perturb', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'class', 'add', 'dev', interface, 'parent', '1:', 'classid', '1:11', 'htb', 'rate', upload_limit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'parent', '1:11', 'handle', '11:', 'sfq', 'perturb', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f'{YELLOW}Please enter the network interface name (example: eth0): {RESET}')
    print(f'{YELLOW}Please enter the desired upload bandwidth (example: 250Mbit): {RESET}')
    print(f'{YELLOW}Please enter the desired download bandwidth (example: 250Mbit): {RESET}')
    print(f'{BLUE}The download bandwidth is limited to {download_limit} and the upload bandwidth is limited to {upload_limit}.{RESET}')


def main():
    parser = argparse.ArgumentParser(description='Limit download and upload bandwidth of TCP users')

    interface = input(f'{YELLOW}Please enter the network interface name (example: eth0): {RESET}')
    upload_limit = input(f'{YELLOW}Please enter the desired upload bandwidth (example: 250Mbit): {RESET}')
    download_limit = input(f'{YELLOW}Please enter the desired download bandwidth (example: 250Mbit): {RESET}')

    limit_bandwidth(interface, upload_limit, download_limit)


if __name__ == '__main__':
    main()