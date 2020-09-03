import csv
import datetime
import json
import sched
import time
import threading

from pynetgear import Netgear


def write_logs(devices: dict, network_usage):
    """
    {'NewTodayConnectionTime': None, 'NewTodayUpload': 1299.0, 'NewTodayDownload': 14812.0,
    'NewYesterdayConnectionTime': None, 'NewYesterdayUpload': 2037.0, 'NewYesterdayDownload': 34794.0,
    'NewWeekConnectionTime': None, 'NewWeekUpload': (3337.0, 476.77), 'NewWeekDownload': (49606.0, 7086.0),
    'NewMonthConnectionTime': None, 'NewMonthUpload': (3337.0, 111.25), 'NewMonthDownload': (49606.0, 1653.0),
    'NewLastMonthConnectionTime': None, 'NewLastMonthUpload': (98926.0, 3297.0), 'NewLastMonthDownload': (997558.0,
    33251.0)}
    """
    with open('data.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)

        datetime_var = datetime.datetime.now()

        item_data = [datetime_var.strftime('%m/%d/%Y'), datetime_var.strftime('%H:%M'),
                     network_usage['NewTodayUpload'] + network_usage['NewTodayDownload'],
                     network_usage['NewTodayUpload'],
                     network_usage['NewTodayDownload']]

        for device in devices:
            item_data.append('1' if device.allow_or_block == 'Allow' else '0')

        writer.writerow(item_data)


with open('./data.json', 'r') as f:
    data = json.load(f)

s = sched.scheduler(time.time, time.sleep)


def logs_start():
    print("Getting attached devices...")
    devices = netgear.get_attached_devices()
    print("Done.")
    print("Getting traffic meter...")
    traffic = netgear.get_traffic_meter()
    print("Done.")
    print("Writing to logs...")
    write_logs(devices, traffic)
    print("Done.")
    print("Waiting for 1 hour before starting again.")
    threading.Timer(3600, logs_start).start()


print("Logging into Netgear.")
netgear = Netgear(password=data['router-password'], host=data['host-ip'], port=data['port'])
# print(netgear.get_traffic_meter())
print("Logged in...")

print("Getting attached devices...")
devices = netgear.get_attached_devices()
print("Done.")
print("Getting traffic meter...")
traffic = netgear.get_traffic_meter()
print("Done.")
print("Writing to logs...")

print('Setting up logs...')
with open('data.csv', 'a+') as csvfile:
    writer = csv.writer(csvfile)
    row = ['Date', 'Time', 'Usage (MB)', 'Today Upload (MB)', 'Today Download (MB)']
    for device in devices:
        row.append(device.name)
    writer.writerow(row)
print('Done')

print(time.ctime())
logs_start()
