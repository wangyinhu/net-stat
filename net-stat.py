#!/usr/bin/env python3
import time
from os import listdir


def human_bytes(B):
    'Return the given bytes as a human friendly KB, MB, GB, or TB string'
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776
    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def print_line(para):
    template = "{:>15}{:>15}{:>15}{:>15}{:>15}"
    print(template.format(*para))


def print_head():
    print_line(('interface', 'send/Sec', 'receive/Sec', 'total send', 'total receive'))


def print_data(para):
    print_line((para[0], *[human_bytes(i) for i in para[1:]]))


net_dir = '/sys/class/net/'


def get_rx(interface):
    with open(net_dir + interface + '/statistics/rx_bytes', 'r') as f:
        c = f.readline()
    return int(c)


def get_tx(interface):
    with open(net_dir + interface + '/statistics/tx_bytes', 'r') as f:
        c = f.readline()
    return int(c)


def print_hi():
    data = {}
    interfaces = [f for f in listdir(net_dir)]
    for interface in interfaces:
        data[interface] = {}
        data[interface]['tx'] = get_tx(interface)
        data[interface]['rx'] = get_rx(interface)
    while True:
        print('\033[1J\033[H\033[?25l', end='')
        print_head()
        for interface in interfaces:
            tx = get_tx(interface)
            rx = get_rx(interface)
            data[interface]['txd'] = tx - data[interface]['tx']
            data[interface]['rxd'] = rx - data[interface]['rx']
            data[interface]['tx'] = tx
            data[interface]['rx'] = rx
            if data[interface]['tx'] or data[interface]['rx']:
                print_data((interface, data[interface]['txd'], data[interface]['rxd'], data[interface]['tx'], data[interface]['rx']))
        print('------\r', end='')
        time.sleep(0.5)
        print('      ')
        time.sleep(0.5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        print_hi()
    except KeyboardInterrupt:
        pass
