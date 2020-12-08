#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Script for Wedos DDNS 
==============================
This script uses Wedos WAPI for modifiing saved IP adress DNS record to actual IP of running device.
Script finds userfull in case you internet provider change your IP adress in random times and you want automatically watch and apply changes.

MANUAL
1)Set up your WEDOS API (Czech): http://kb.wedos.com/wapi/aktivace-nastaveni.html
2)Set your credentials few lines bellow.
3)Run this daily by cron.
This was tested on Python 3 only and requires requests.


Modified version by:
Copyright (c) 2020 Marek Vach <mvach@email.cz>

Original software by:
Copyright (c) 2015 Miro Hrončok <miro@hroncok.cz>
https://gist.github.com/hroncok/166305c39fd8e80609d1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
Provided license texts might have their own copyrights and restrictions
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import datetime
import hashlib
import json
import socket

import requests

import urllib.request

# Change these!
LOGIN = 'user@example.com' #CASE SENSITIVE!
PASSWORD = 'passW0rd!' # by Wedos requirments must contain at least one upper case and one special symbol
DOMAIN = 'example.com' # 'example.com' - must be already existing A record!

# Keep this
API = 'https://api.wedos.com/wapi/json'


def get_auth(login=LOGIN, password=PASSWORD):
    passhash = hashlib.sha1(password.encode('utf8')).hexdigest()
    phrase = login + passhash + datetime.datetime.now().strftime('%H')
    return hashlib.sha1(phrase.encode('utf8')).hexdigest()


def request(command, data, login=LOGIN, auth=get_auth(), url=API):
    d = {'request': {'user': login, 'auth': auth, 'command': command, 'data': data}}
    r = requests.post(url, data={'request': json.dumps(d)})
    data = r.json()
    if data['response']['result'] != 'OK':
        raise Exception('Response from WEDOS was {}'.format(data['response']['result']))
    return data


def dns_rows_list(domain=DOMAIN):
    return request('dns-rows-list', locals())


def dns_row_update(row_id, ttl, rdata, domain=DOMAIN):
    return request('dns-row-update', locals())


def dns_domain_commit(name=DOMAIN):
    return request('dns-domain-commit', locals())


def find_A_record():
    data = dns_rows_list()

    for row in data['response']['data']['row']:
        if row['rdtype'] == 'A' and row['name'] == '':
            return row['ID'], row['ttl']

    raise Exception('Cannot find A record for the domain')


def update_A_record(ip, domain=DOMAIN):
    dns_row_update(*find_A_record(), rdata=ip)
    dns_domain_commit()
    print('Updated {} to {}'.format(domain, ip))

def get_current_device_public_ip():
    ident_me_find_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return ident_me_find_ip

def compare_ip_of_dns_record_and_local_device_and_make_changes(domain=DOMAIN):
    dns_ip = socket.gethostbyname(domain)
    local_device_ip = get_current_device_public_ip()

    if dns_ip != local_device_ip:
        update_A_record(local_device_ip, domain)
    else:
        print('IP addresses match')


compare_ip_of_dns_record_and_local_device_and_make_changes()
