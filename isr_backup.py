#!/usr/bin/env python3
import getpass
from ncclient import manager
from pathlib import Path
from netmiko import ConnectHandler
import concurrent.futures
import pyinputplus as pyip
import sys
import argparse

''' isrbackup allows user to backup running configuration of multiple Cisco devices without having to log into them individually.
 It is able to concurrently access multiple devices, retreive their running config and save to an "isr_backups" folder.'''


def get_args():
    """get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Pings IP addresses entered or from file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    
    parser.add_argument('-f',
                        '--file',
                        help='Input file - listing device name and ip address pairs',
                        metavar='str',
                        type=str
                        )

    parser.add_argument('-p',
                        '--port',    
                        help='netconf port number',
                        metavar='str',
                        type=str)

    return parser.parse_args()


def From_file_to_list(filename):
    mylist = []
    try:        
        # Parses text file to a list of the lines
        with open(filename, 'r') as ftext:
            flist = ftext.readlines()
            mylist = [i[:-1] for i in flist]
        print('Loaded File to List.')
    except Exception as err:
        print('file error: ' + err)
    return mylist


class Device:
    # class methods as alternative constructor
    # using to create Device object
    def __init__(self, ip, hostname):
        self.ip = ip
        self.hostname = hostname

    @classmethod
    def from_string(cls, dev_str):
        ip, hostname = dev_str.split()
        return cls(ip, hostname)


def Create_obj_lst(dev_list):
    # Creates objects using input list
    obj_list = []
    for i in dev_list:
        print(i)
        obj_list.append(Device.from_string(i))

    return obj_list


def create_folder():
    # Creates the folder for storing config files
    if ((Path.cwd() / 'isr_backups')).exists() == False:
        print('Creating folder.. ')
        Path(Path.cwd() / 'isr_backups').mkdir()


def create_file(name_offile, content):
    # creates file in specified location
    file_location = Path.cwd() / 'isr_backups' / name_offile
    with open(file_location, 'w') as f:
        # converting to string before writing by attributes .xml or .data_xml
        f.write(content.xml)
        print(name_offile + ' done')


def nccconnect(host_rtr, user, pw, nport=22):
    # ncclient login parameters
    try:
        net_conn = manager.connect(
            host=host_rtr,
            port=nport,
            username=user,
            password=pw,
            hostkey_verify=False,
            timeout=15)
    except Exception as err:
        print(err)
        net_conn = 'connection error'

    return net_conn


def netconf_backup(dev_obj, user, pw, nport=22):
    ''' takes in a device object and gets device config 
    uses ncclient and creates xml copy of running config'''
    try:
        connct = nccconnect(dev_obj.ip, user, pw, nport)
        ios_conf = connct.get_config(source='running')
        hsname = dev_obj.hostname + '.xml'
        create_file(hsname, ios_conf)
        
    except Exception as exc:
        print(f'Error: {dev_obj.ip}: unable to create file')
    return


def provision_dev(device, config_commands, param):
    '''Provisions cisco device; uses netmiko to connect and send commands '''
    param['host'] = device.ip
    try:
        net_connect = ConnectHandler(**param)
        output = net_connect.send_config_set(config_commands)
        print(device.ip + ' ..config done')
    except Exception as exc:
        print(f'There was a problem with {device.ip}: {exc}')
    net_connect.disconnect()
    return


def concurrent_backup(fxn, obj_lst, user, pw, nport, count):
    # performs concurrent backups with threads across the list of routers
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
        for i in obj_lst:
            executor.submit(fxn, i, user, pw, nport)


def concurrent_commands(fxn, obj_lst, cmd, param, count):
    # performs concurrent configuration with threads across the list of routers
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
        for i in obj_lst:
            executor.submit(fxn, i, cmd, param)

# ----------------------------------------------------------------------

if __name__ == '__main__':

    args = get_args()

    print()
    print('#' * 42)
    print(('#' * 3) + '  --    Running ISR BACKUP     ---  ' + ('#' * 3))
    print(('#' * 42) + '\n')


    user = input('username: ')
    pw = getpass.getpass()
    

    if args.port:
        netconf_port = args.port
    else:
        netconf_port = input('Enter netconf port number: ')

    if args.file:
        routerfile = args.file
    else:
        routerfile = input('Enter filename: ')


    if netconf_port == '':
        netconf_port = 22
    # connection parameters for netmiko
    dev_param = {'device_type': 'cisco_ios',
                'host': '',
                'username': user,
                'password': pw,
                'timeout': 15,
                'global_delay_factor': 0.5
                }


    # list of ios commands to send to devices
    commands_netconf = ['netconf ssh', 'do wr']
    try:
        rtr_list = From_file_to_list(routerfile)
        create_folder()
        rtr_obj_list = Create_obj_lst(rtr_list)

        ask_netconf = pyip.inputYesNo(
            'Will you need to enable netconf ? [Y or N]: ')
        if ask_netconf == 'yes':
            print('Enabling netconf..')
            concurrent_commands(provision_dev, rtr_obj_list,
                                commands_netconf, dev_param, 50)
        else:
            print('netconf already enabled on routers' + '\n')

        print('Intitiating backup..')
        concurrent_backup(netconf_backup, rtr_obj_list, user, pw, netconf_port, 50)
    
    except ValueError: 
        print('file err: file should not end with empty line or space')
    

    except Exception as exc:
        print('There was a problem: %s' % (exc))

    

    print('\nDone.')
    end = input('Hit Enter to close: ')
