# **EventBot: Eventbrite Ticket Automation**

The current setup script/process only works in Linux/OS X environments. If using Windows, use Windows Subsystem for Linux (WSL).

Run EventBot any time prior to a ticket sale.

**WARNING**: This is not a guarantee. EventBot should be used in combination with manually attempting to get tickets in your normal browser.

## Usage

```
usage: eventbot.py [-h] [-id ID] [-num NUM] [--wait WAIT] url

Eventbrite bot to automate securing event tickets

positional arguments:
  url          Eventbrite event URL

optional arguments:
  -h, --help   show this help message and exit
  -id ID       Ticket ID to purchase
  -num NUM     Number of tickets to purchase
  --wait WAIT  Seconds the browser should wait for DOM to load
```

Pass the bot an Eventbrite event URL:<br>
`python eventbot.py https://www.eventbrite.com/e/muddfest-fresno-with-puddle-of-mudd-saliva-trapt-saving-abel-tantric-tickets-60614998091`

## Building the Environment

Prerequisites:<br>
```
# python 2.7
# python-pip
# wget
```

Run the install script:<br>
`./install.sh`

**OR** manually set up selenium:<br>
```
$ pip install selenium
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
$ tar -xvf geckodriver-v0.24.0-linux64.tar.gz
$ export PATH=$PATH:/path/to/geckodriver/directory
```

## TODO

* Add support for varying event pages (i.e. tickets displayed in table, not modal)
* Add support for auto-filling payment information based on config file