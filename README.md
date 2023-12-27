# Pi Hole DNS Checker and Updater
This is intended to be used with pihole for devices that have a physical MAC and wireless MAC so obtain separate IP addresses in a typical network. This script can run every 5 minutes on the pihole and configure an online IP address to the specific DNS name. This can help with automations, configurations, and integrations. 

Some examples of uses is with Cameras that can be wired or wireless, these can then be moved around and NVR configurations would simply point at the DNS name and not need to be altered.

This is just one usecase but there are many.

Usage:
```
python dnschecker.py <ip_1> <ip_2> <dns_name>
```
```
*/5 * * * * sudo python3 dnschecker.py 192.168.1.72 192.168.1.202 porchcam.lan
```
