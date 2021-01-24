#!/usr/bin/env python3
from time import time, sleep
import os

from transip import TransIP
from transip.exceptions import TransIPError


def update_dns(client, name, address):
    """
    Ensure all DNS A-records of a single domainname have the correct IP-address
    as there content.

    Args:
        client (transip.TransIP): The TransIP API client.
        name (str): The domainname.
        address (str): The IP-address.
    """
    domain = client.domains.get(name)

    # List all DNS records of the domain
    records = domain.dns.list()

    updates = False
    for record in records:
        if record.type == "A" and record.content != address:
            print(f"{record.name} record is using an old IP: {record.content}")
            # Set the content of the A-record to the specified address
            record.content = address
            updates = True

    # Only attempt to update the DNS records when changes where made to the
    # existing records.
    if updates:
        print("Updating DNS records")
        try:
            domain.dns.replace(records)
        except TransIPError as exc:
            print("Failed to update DNS records!")
        finally:
            print("DNS records successfully updated!")

    print("All records are up to date!")


def main():
    print("Starting TransIP DNS Updater...")

    # Get the variables set within Docker
    username = os.environ['username']
    domain = os.environ['domain']
    keyfile = '/keyfile/key'

    print("Checking if keyfile is present...")
    if os.path.isfile(keyfile):
        print("Key found!")
    else:
        print("No key provided, exiting...")
        return

    # Get the current external IP
    extIP = get('https://ipapi.co/ip/').text

    # Client to connect to the TransIP API
    client = TransIP(login=username, private_key_file=keyfile)

    while True:
        sleep(60 - time() % 60)
        try:
            update_dns(client, domain, extIP)
        except TransIPError as exc:
            print(f"Failed to update the DNS records: {exc}")


if __name__ == '__main__':
    main()
