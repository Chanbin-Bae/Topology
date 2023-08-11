import sys
#sys.path.append("/home/mnc/mininet/")
sys.path.append("/home/p4/mininet")
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import p4_mininet
from p4_mininet import P4Switch, P4Host
import math

import argparse
from time import sleep
import os
import subprocess
from subprocess import PIPE

# _Default_K = 4

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 9300

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                   type=str, action="store", required=True)
parser.add_argument('--l2switch', help='Path to bftswitch JSON config file',
                   type=str, action="store", required=True)
parser.add_argument('--selswitch', help='Path to bftswitch JSON config file',
                   type=str, action="store", required=True)            
parser.add_argument('--cli', help='Path to BM CLI',
                   type=str, action="store", required=True)

args = parser.parse_args()

class MyTopo(Topo):
    def __init__(self, sw_path, l2switch, selswitch, **opts):
        # Initialize topology with creating switches
        #k = int(t)
        Topo.__init__(self, **opts)
        count = 1
        switches = []
        hosts = []

        linkopts = dict(bw=1, delay='1ms', loss=0, use_htb=True)

        #switch1
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch2
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch3
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch4
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch5
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch6
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch7
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch8
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch9
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1
        #switch10
        switches.append(self.addSwitch('switch%d' % (count),
                                sw_path = sw_path,
                                json_path = l2switch,
                                thrift_port = _THRIFT_BASE_PORT + count,
                                pcap_dump = False,
                                device_id = count))
        count = count + 1

       #switch-switch links.
        self.addLink(switches[0], switches[4],**linkopts)
        self.addLink(switches[0], switches[5],**linkopts)
        self.addLink(switches[1], switches[4],**linkopts)
        self.addLink(switches[1], switches[5],**linkopts)
        self.addLink(switches[2], switches[6],**linkopts)
        self.addLink(switches[2], switches[7],**linkopts)
        self.addLink(switches[3], switches[6],**linkopts)
        self.addLink(switches[3], switches[7],**linkopts)
        self.addLink(switches[4], switches[8],**linkopts)
        self.addLink(switches[5], switches[8],**linkopts)
        self.addLink(switches[6], switches[8],**linkopts)
        self.addLink(switches[7], switches[8],**linkopts)
        self.addLink(switches[4], switches[9],**linkopts)
        self.addLink(switches[5], switches[9],**linkopts)
        self.addLink(switches[6], switches[9],**linkopts)
        self.addLink(switches[7], switches[9],**linkopts)
        

        # Create hosts and link to appropriate edge hosts.
               
        for i in range (0,16):
            hosts.append(self.addHost('host%d' % (i)))


        for i in range(0,4):
            self.addLink(hosts[i], switches[0],**linkopts)
            
        for i in range(4,8):
            self.addLink(hosts[i], switches[1],**linkopts)

        for i in range(8,12):
            self.addLink(hosts[i], switches[2],**linkopts)

        for i in range(12,16):
            self.addLink(hosts[i], switches[3],**linkopts)

        # self.addLink(hosts[0], switches[0],**linkopts)
        # self.addLink(hosts[1], switches[0],**linkopts)
        # self.addLink(hosts[2], switches[1],**linkopts)
        
        # for i in range(0,4):
        #     for j in range (0,3):
        #         self.addLink(hosts[3*i+j], switches[6+i],**linkopts)

def main():
   topo = MyTopo(args.behavioral_exe, args.l2switch, args.selswitch)

   net = Mininet(topo = topo,
                   host = P4Host,
                   switch = P4Switch,
                   link=TCLink,
                   controller = None )

   net.start()
   print("netstart end")
   sleep(2)
   print("Ready !")
   CLI( net )
   net.stop()

if __name__ == '__main__':
   setLogLevel( 'info' )
   # setLogLevel( 'debug' )
   main()
