#!/usr/bin/env python3
# vim: set ft=python3
import re
import sys
import http.client
import datetime
import subprocess

# Please change this to your username:
username = "ztygalaxy"


def download_stat():
    start = (datetime.datetime.now() - datetime.timedelta(days=3 * 365)).strftime(
        "%Y-%m-%d"
    )
    end = datetime.datetime.now().strftime("%Y-%m-%d")

    conn = http.client.HTTPSConnection("github.com")

    payload = ""

    headers = {
        "connection": "keep-alive",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "dnt": "1",
        "x-requested-with": "XMLHttpRequest",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://github.com/{}/".format(username),
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,de;q=0.5,ko;q=0.4,mt;q=0.3",
    }

    conn.request(
        "GET",
        "/users/{}/contributions?from={}&to={}".format(username, start, end),
        payload,
        headers,
    )

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def parse_xml(xml):
    """convert data to a dict, key is dateime, value is int for commit numebrs"""
    match = re.findall(r'<rect.*data-count="(\d+)".*data-date="([\d-]+)".*', xml)
    data = {k: v for v, k in match}
    count = {}

    for key, value in data.items():
        date_key = datetime.datetime.strptime(key, "%Y-%m-%d")
        count[date_key] = int(value)
    return count


def get_first_uncommited_day(stat_data):
    for date in sorted(stat_data.keys()):
        if stat_data[date] == 0:
            return date


raw_data = download_stat()
stat = parse_xml(raw_data)
commit_date = get_first_uncommited_day(stat)
print("Commit date is: {}".format(commit_date.strftime("%Y-%m-%d")))

subprocess.run(
    ["git", "commit", "--date={}".format(commit_date.timestamp()),] + sys.argv
)
