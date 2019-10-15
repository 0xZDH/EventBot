#!/usr/bin/env python

""" Eventbrite bot to automate securing event tickets. """

import sys
import time
import argparse
from browser.engine import *

# Eventbrite seems to change these values, so lets keep track here in case we need to update
TICKET_BUTTON   = '.micro-ticket-box__btn'
IFRAME_ID       = '#eventbrite-widget-modal-{ID}'  # Uses event ID in URL
TICKET_ID       = '#ticket-quantity-selector-{ID}' # Uses ticket ID found in JS on page
CHECKOUT_BUTTON = '.eds-btn'


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Eventbrite bot to automate securing event tickets")
        parser.add_argument("url",    type=str, help="Eventbrite event URL")
        parser.add_argument("-id",    type=str, help="Ticket ID to purchase")
        parser.add_argument("-num",   type=str, help="Number of tickets to purchase")
        parser.add_argument("--wait", type=int, help="Seconds the browser should wait for DOM to load")
        args = parser.parse_args()

        url    = args.url.split('?')[0]
        url_id = IFRAME_ID.format(ID=url.split('-')[-1])
        wait   = 2 if not args.wait else args.wait

        if not args.id or not args.num:
            print("[!] Missing Ticket ID and Number of tickets...")
            answer = str(raw_input("Would you like to run the ticket tool? (Y/N) ")).lower().strip()
            if answer[:1] =='y':
                from tickets import *
                t = Tickets(url)
                t.get_tickets()
                t.show_tickets()
                ticket_id,num_tickets = t.ask()
                ticket_id = TICKET_ID.format(ID=ticket_id)

            else:
                parser.error("Ticket ID and number of tickets required.")

        else:
            ticket_id   = TICKET_ID.format(ID=args.id)
            num_tickets = args.num

        print("[*] Initializing browser...")
        browser = BrowserEngine(wait=wait)

        print("[*] Requesting URL: %s" % url)
        browser.get_request(url)

        print("[*] Waiting for page to fully load...")
        time.sleep(3) # Let the whole page load before clicking, since this happens once, a sleep is fine

        print("[*] Checking for available tickets...")

        while True:

            browser.clear_cookies() # So memory usage doesn't sky rocket

            if browser.get_element("CSS_SELECTOR", TICKET_BUTTON):
                print("[*] Opening ticket options...")
                browser.click_button(browser.get_element("CSS_SELECTOR", TICKET_BUTTON))

            if browser.get_element("CSS_SELECTOR", url_id):
                print("[*] Switching context to ticket iFrame...")
                browser.switch_context(browser.get_element("CSS_SELECTOR", url_id))

            if browser.get_element("CSS_SELECTOR", ticket_id):
                print("[+] Selecting %s tickets..." % num_tickets)
                browser.select_dropdown(browser.get_element("CSS_SELECTOR", ticket_id), num_tickets)

                print("[*] Going to checkout...")
                browser.click_button(browser.get_element("CSS_SELECTOR", CHECKOUT_BUTTON))
                print("[*] Now that the tickets have been reserved for several minutes, go get em!")
                _ = raw_input("Once you have completed purchasing your tickets, press <ENTER> to cleanly exit the browser instance...")
                browser.quit_driver()
                break

            else:
                print("[*] No dice, refreshing...")
                browser.refresh()

    except KeyboardInterrupt:
        print("\n[*] Exitting...")
        try:
            browser.quit_driver()

        except:
            pass