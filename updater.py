#!/usr/bin/env python3
from transip.service.domain import DomainService
from transip.service.objects import DnsEntry
from pathlib import Path
from requests import get
from time import time, sleep
import os

# Print startup to console
print("Starting TransIP DNS Updater...")

# Check if keyfile exists
print("Checking if keyfile is present...")
try:
    with open('/keyfile/key') as x:
        print("Key found!")
except IOError:
    print("No key provided, exiting...")
    exit()
    
# Get the variables set within Docker
username = os.environ['username']
domain = os.environ['domain']
keyfile = '/keyfile/key'

# Get the current external IP
extIP = get('https://ipapi.co/ip/').text

# Client to connect to the TransIP API
client = DomainService(username, private_key_file=keyfile)

# Update the DNS
def update_dns():
  for entry in client.get_info(domain).dnsEntries:
    if entry.type == "A":
      if entry.content != extIP:
        print(entry.name + " record is using an old IP: " + entry.content)

        # DNS Entry list with current external IP
        oldList = []
        list = DnsEntry(entry.name, entry.expire, entry.type, entry.content)
        oldList.append(list)
        # Remove old DNS entry
        print("Removing old entry...")
        client.remove_dns_entries(domain, oldList)

        # DNS Entry list with new external IP
        newList = [] 
        list = DnsEntry(entry.name, entry.expire, entry.type, extIP)
        newList.append(list)
        # Add new DNS entry
        print("Creating new entry...")
        client.add_dns_entries(domain, newList)
        print("New entry created successfully!")
  print("All records are up to date! \n")
#endDef
  
while True:
    sleep(60 - time() % 60)
    update_dns()
#EOF