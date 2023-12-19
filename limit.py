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

    interface = input("لطفاً نام رابط شبکه را وارد کنید (مثلاً eth0): ")
    upload_limit = input("لطفاً پهنای باند آپلود مورد نظر را وارد کنید (مثلاً 1Mbit): ")
    download_limit = input("لطفاً پهنای باند دانلود مورد نظر را وارد کنید (مثلاً 2Mbit): ")

    limit_bandwidth(interface, upload_limit, download_limit)


if __name__ == '__main__':
    main()