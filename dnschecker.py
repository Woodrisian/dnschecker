#!/usr/bin/python3
import sys
import socket
import subprocess
import time
import requests

WEBHOOK_URL ="https://discordapp.com/api/webhooks/[YOUR STUFF HERE]"

def send_discord_msg(WEBHOOK_URL, msg):
  data = { "content": msg}
  requests.post(WEBHOOK_URL, data=data)


def check_server(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        return True
    except (socket.error, socket.timeout):
        return False

def read_custom_list():
    try:
        # Run this on your pihole
        with open("/etc/pihole/custom.list", "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def write_custom_list(entries):
    with open("/etc/pihole/custom.list", "w") as file:
        for entry in entries:
            file.write(entry + "\n")

def restart_pihole_dns():
    subprocess.call(["pihole", "restartdns"])

def update_dns_entry(server_ip, dns_name, existing_entries):
    new_entry = "{} {}".format(server_ip, dns_name)
    old_entry = ""

    if(new_entry in existing_entries):
        print("Entry already exists in custom.list")
        exit()

    for i, entry in enumerate(existing_entries):
        if dns_name in entry:
            old_entry = existing_entries[i]
            # Remove existing entry with the same DNS name
            existing_entries.pop(i)
            break

    if(old_entry!=""):
        print(old_entry+" went offline, adding new online entry: "+new_entry)
        send_discord_msg(WEBHOOK_URL, old_entry+" went offline, adding new online entry: "+new_entry)
    else:
        print("New entry "+server_ip+" being added for "+dns_name)
        send_discord_msg(WEBHOOK_URL, "New entry "+server_ip+" being added for "+dns_name)

    existing_entries.append(new_entry)
    print(existing_entries)

    write_custom_list(existing_entries)
    restart_pihole_dns()
    print("Updated custom DNS entry.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python dnschecker.py <ip_1> <ip_2> <dns_name>")
        sys.exit(1)

    SERVER1 = sys.argv[1]
    SERVER2 = sys.argv[2]
    DNS_NAME = sys.argv[3]

    while True:
        if check_server(SERVER1, 80):
            update_dns_entry(SERVER1, DNS_NAME, read_custom_list())
        elif check_server(SERVER2, 80):
            update_dns_entry(SERVER2, DNS_NAME, read_custom_list())
        else:
            print("Both IPs are down.")

