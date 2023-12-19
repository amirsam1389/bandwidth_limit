#!/usr/bin/env python3

import argparse
import subprocess


def limit_bandwidth(interface, upload_limit, download_limit):
    subprocess.run(['tc', 'qdisc', 'del', 'dev', interface, 'root'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'root', 'handle', '1:', 'htb', 'default', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'class', 'add', 'dev', interface, 'parent', '1:', 'classid', '1:10', 'htb', 'rate', download_limit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'parent', '1:10', 'handle', '10:', 'sfq', 'perturb', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'class', 'add', 'dev', interface, 'parent', '1:', 'classid', '1:11', 'htb', 'rate', upload_limit], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['tc', 'qdisc', 'add', 'dev', interface, 'parent', '1:11', 'handle', '11:', 'sfq', 'perturb', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f'پهنای باند دانلود محدود به {download_limit} و پهنای باند آپلود محدود به {upload_limit} شد.')


def main():
    parser = argparse.ArgumentParser(description='محدود کردن پهنای باند دانلود و آپلود کاربران TCP')
    parser.add_argument('-i', '--interface', required=True, help='نام رابط شبکه (مثلاً eth0)')
    parser.add_argument('-u', '--upload', required=True, help='پهنای باند آپلود مورد نظر (مثلاً 1Mbit)')
    parser.add_argument('-d', '--download', required=True, help='پهنای باند دانلود مورد نظر (مثلاً 2Mbit)')
    args = parser.parse_args()

    limit_bandwidth(args.interface, args.upload, args.download)


if __name__ == '__main__':
    main()