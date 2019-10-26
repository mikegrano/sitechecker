'''Site checker v1
currently supports following inputs: cmdline and json file
'''

import socket
import urllib.request
import json
import argparse

#Global variables
domain=0
ip=0

#Table formatting
def get_pretty_table(iterable, header):
    max_len = [len(x) for x in header]
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        for index, col in enumerate(row):
            if max_len[index] < len(str(col)):
                max_len[index] = len(str(col))
    output = '-' * (sum(max_len) + 1) + '\n'
    output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    return output

#Resolves dns name
def dnscheck():
    global site, domain, ip
    domain = site.split("www.", 1)[1]
    print("Checking DNS for", domain)
    ip = socket.gethostbyname(domain)
    getstatuscode()

#GET request and retrieve HTTP status code
def getstatuscode():
    global site, domain, ip
    resp = urllib.request.urlopen(site)
    print(get_pretty_table([[site, ip, resp.getcode()]], ['Site', 'Address', 'Status']))

#Loads json input into list, iterates over elements
def jsonsitecheck():
    with open(jsonpath) as json_file:
        data = json.load(json_file)
        vals = list(data.values())
        print(vals)
        results = []
        for i in vals[0]:
            dom = i.split("www.", 1)[1]
            print("Checking DNS for", dom)
            ipadd = socket.gethostbyname(dom)
            print("The address is ", ipadd)
            resp = urllib.request.urlopen(i)
            status = resp.getcode()
            oneliner = str(str(i) + " | " + str(ipadd) + " | Status: " + str(status))
            results.append(oneliner)
        print("\n".join(results))

#Initialize argparser
parser = argparse.ArgumentParser(description='SiteCheckerv1')
parser.add_argument("--h", help="--q to quit, --json <path> for json input, --site <http://www.example.com> for cmdline input")
parser.add_argument("--json", type=str, help="Full path (/) to json file")
parser.add_argument("--site", type=str, help="Site name <http://www.example.com>")
args = parser.parse_args()
site = args.site
jsonpath = args.json

#Selectively call functions based on cli arguments
if args.site:
    dnscheck()
if args.json:
    jsonsitecheck()

'''Def boilerplate NOT IN USE
if __name__ == "__main__":
    main()
'''
