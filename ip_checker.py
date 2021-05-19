from os import system
from platform import system as get_os_name
from time import sleep
from requests import get
from datetime import datetime
from regex import compile as re

ips_changed = 0
valid_ipv4 = re(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
timer = datetime.now()
clearing_str = 'cls' if get_os_name() == 'Windows' else 'clear'

try:
    from pandas import DataFrame, Series
    from numpy import nan
    my_ips = DataFrame(
        columns=['isp', 'loc', 'latest_time'],
        index=Series(dtype=str, name='ip')
    )

    while True:
        try:
            current_ip = get('http://www.ipinfo.io').json()
            if current_ip.get('status') in (429,):
                break
            my_ips.loc[current_ip.get('ip', nan)] = [
                current_ip.get('org', nan),
                current_ip.get('loc', nan),
                datetime.now()
            ]
            attempt = 0
        except:
            attempt += 1
            if attempt > 30:
                break
            continue
        current_ip = current_ip.get('ip', nan)
        current_time = my_ips.loc[current_ip, 'latest_time']
        period = (current_time - timer).total_seconds()
        if valid_ipv4.search(current_ip):
            try:
                if previous_ip != current_ip:
                    ips_changed += 1
            except NameError:
                pass
            previous_ip = current_ip
            my_ips.sort_values(
                'latest_time', 
                ascending=False, 
                inplace=True
            )
            if not int(period) % 15:
                system(clearing_str)
                print(current_time.strftime('%d %b %Y %H%M'))
                cps = ips_changed / period
                if int(round(cps * 60, 0)):
                    cps = int(round(cps, 0))
                    print('dynamic', cps, 'changes per second')
                    current_ips = my_ips.iloc[:cps+1]
                else:
                    print('static')
                    current_ips = my_ips.iloc[:1]
                for ip, info in current_ips.apply(
                    lambda vals: ' '.join([
                        str(val) 
                        for val in vals
                        if not val is nan
                    ]), 
                    axis='columns'
                ).iteritems():
                    print(ip, info, sep=' @ ')
                previous_ips = my_ips.loc[~my_ips.index.isin(
                    current_ips.index
                )]
                previous_ips.sort_index(inplace=True)
                for ip in previous_ips.index:
                    print(ip)
        else:
            break
        sleep(1)

except ModuleNotFoundError:
    my_ips = set()

    while True:
        try:
            current_ip = get('http://www.ipinfo.io').json()
            if current_ip.get('status') in (429,):
                break
            current_ip = ' '.join([
                current_ip.get('ip', ''),
                '@', current_ip.get('org', ''),
                current_ip.get('loc')
            ])
            attempt = 0
        except:
            attempt += 1
            if attempt > 30:
                break
            continue
        current_time = datetime.now()
        period = (current_time - timer).total_seconds()
        if valid_ipv4.search(current_ip):
            try:
                if previous_ip != current_ip:
                    ips_changed += 1
            except NameError:
                pass
            previous_ip = current_ip
            my_ips |= {current_ip}
            if not int(period) % 15:
                system(clearing_str)
                print(current_time.strftime('%d %b %Y %H%M'))
                cps = int(round(ips_changed / period, 0))
                if cps:
                    print('dynamic', cps, 'changes per second')
                else:
                    print('static')
                print(len(current_ip)*'-', current_ip, len(current_ip)*'-', sep='\n')
                for ip in sorted(my_ips - {current_ip}):
                    print(ip)
        else:
            break
        sleep(1)

print(get('http://www.ipinfo.io').json())