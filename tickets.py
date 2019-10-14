#!/usr/bin/env python

import re
import json
import urllib3
import argparse
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tickets:

    # Keep track of changing data
    delim    = '{"public_id"'
    id_delim = '_'
    id_num   = 1

    def __init__(self, url):
        self.url     = url
        self.tickets = {}

    def ask(self):
        _idb,numb = False,False
        _max = 0

        while not _idb:
            _id = str(raw_input("Please select a ticket ID: ")).strip()
            for ticket in self.tickets.keys():
                if _id == self.tickets[ticket][0]:
                    _idb = True
                    _max = self.tickets[ticket][2]
                    break

        while not numb:
            num = int(str(raw_input("Please select a number of tickets to purchase (up to %s): " % _max)).strip())
            if 0 < num <= int(_max):
                numb = True

        return (_id, str(num))

    def show_tickets(self):
        print('*** TICKETS ***\n')
        for ticket in self.tickets.keys():
            print('%s:' % ticket)
            print('\tCost: %s\n\tMax Tickets: %s\n\tID: %s' % (self.tickets[ticket][1], self.tickets[ticket][2], self.tickets[ticket][0]))


    def get_tickets(self):
        resp = requests.get(self.url, verify=False)
        collection = re.search('collection : \[(.*)\]', resp.text).group(1)

        quant = []
        for obj in collection.split(',' + self.delim):
            quant.append(self.delim + obj if self.delim not in obj else obj)

        for obj in quant:
            a = json.loads(obj)
            if 'maximum_quantity' in a.keys(): _max = a['maximum_quantity']
            elif 'maximum_quantity_per_order' in a.keys(): _max = a['maximum_quantity_per_order']
            else: _max = '0'
            cost = a['locale_aware_cost_display']
            name = a['variants'][0]['display_name']
            _id  = a['ticket_form_element_name'].split(self.id_delim)[self.id_num]
            self.tickets[name] = [_id, cost, _max]


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python tickets.py <URL>")
        sys.exit()

    t = Tickets(sys.argv[1])
    t.get_tickets()
    t.show_tickets()

    # Testing
    _id,num = t.ask()
    print(_id)
    print(num)