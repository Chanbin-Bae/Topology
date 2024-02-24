import argparse
from p4utils.mininetlib.network_API import NetworkAPI
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.link import TCLink
from multiprocessing import Process
from time import sleep
import subprocess

# Modify directory
default_rule = 'rules/20240222/'

# Run command on Mininet node
def run_command_on_host(host_node, command):
    result = host_node.cmd(command)

# Configure Network
def config_network(p4):
    net = NetworkAPI()

    # If want to use Mininet CLI, modify to True
    net.cli_enabled = False
    
    # Link option
    linkops = dict(bw=1000, delay='1ms', loss=0, use_htb=True)

    # Network general options
    net.setLogLevel('info')
    
    # Generate P4 switch with rules
    net.addP4Switch('s1',cli_input= default_rule + 's1-commands.txt')
    net.addP4Switch('s2',cli_input= default_rule + 's2-commands.txt')
    net.addP4Switch('s3',cli_input= default_rule + 's3-commands.txt')
    net.addP4Switch('s4',cli_input= default_rule + 's4-commands.txt')
    net.addP4Switch('s5',cli_input= default_rule + 's5-commands.txt')
    net.addP4Switch('s6',cli_input= default_rule + 's6-commands.txt')
    net.addP4Switch('s7',cli_input= default_rule + 's7-commands.txt')
    net.addP4Switch('s8',cli_input= default_rule + 's8-commands.txt')
    net.addP4Switch('s9',cli_input= default_rule + 's9-commands.txt')
    net.addP4Switch('s10',cli_input= default_rule + 's10-commands.txt')

    # Execute P4 program on switch
    net.setP4SourceAll(p4)

    # Generate hosts
    hosts = []
    for i in range (0,4):
        hosts.append(net.addHost('h%d' % (i+1)))    
    
    net.addLink('h1', 's1',**linkops)
    net.addLink('h2', 's2',**linkops)
    net.addLink('h3', 's3',**linkops)
    net.addLink('h4', 's4',**linkops)
        
    net.addLink('s1', 's5',**linkops)
    net.addLink('s1', 's6',**linkops)
    
    net.addLink('s2', 's5',**linkops)
    net.addLink('s2', 's6',**linkops)

    net.addLink('s3', 's7',**linkops)
    net.addLink('s3', 's8',**linkops)

    net.addLink('s4', 's7',**linkops)
    net.addLink('s4', 's8',**linkops)
    
    net.addLink('s5', 's9',**linkops)
    net.addLink('s5', 's10',**linkops)
    
    net.addLink('s6', 's9',**linkops)
    net.addLink('s6', 's10',**linkops)

    net.addLink('s7', 's9',**linkops)
    net.addLink('s7', 's10',**linkops)

    net.addLink('s8', 's9',**linkops)
    net.addLink('s8', 's10',**linkops)

    # Assignment strategy
    net.mixed()

    # Nodes general options: Log, Pcap ,,,
    net.enableCpuPortAll()
    
    return net

# Parser for P4 program and number of sending packets
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p4', help='p4 src file.',
                        type=str, required=False, default='p4src/int_mri.p4')
    parser.add_argument('--c', help='number of packets',
                        type=int, required=False, default=10000)
    return parser.parse_args()


def main():
    args = get_args()
    net = config_network(args.p4)
    net.startNetwork()
        
    # Use for INT Collector, Execute on VM host at different terminals
    commands1 = [
        "sudo gnome-terminal --tab --title='s1' -- bash -c 'python3 /home/p4/INT/QINT/QINT_P4/receive_report.py --i s1-cpu-eth1; exec bash'",
        "sudo gnome-terminal --tab --title='s2' -- bash -c 'python3 /home/p4/INT/QINT/QINT_P4/receive_report.py --i s2-cpu-eth1; exec bash'",
        "sudo gnome-terminal --tab --title='s3' -- bash -c 'python3 /home/p4/INT/QINT/QINT_P4/receive_report.py --i s3-cpu-eth1; exec bash'",
        "sudo gnome-terminal --tab --title='s4' -- bash -c 'python3 /home/p4/INT/QINT/QINT_P4/receive_report.py --i s4-cpu-eth1; exec bash'",
    ]
    for command in commands1:
        subprocess.run(command, shell=True)
    sleep(2)
    
    
    # Execute command on Mininet nodes simultaneously
    commands2 = []
    for i in range(0,4):
        command = 'python3 /home/p4/INT/QINT/QINT_P4/Packet/send_test.py --host h{0}'.format((i+1))
        commands2.append(command)

    processes = []
    process1 = Process(target=run_command_on_host, args=(net.net.get('h1'), commands2[0]))
    process1.start()
    processes.append(process1)

    process2 = Process(target=run_command_on_host, args=(net.net.get('h2'), commands2[1]))
    process2.start()    
    processes.append(process2)

    process3 = Process(target=run_command_on_host, args=(net.net.get('h3'), commands2[2]))
    process3.start()
    processes.append(process3)

    process4 = Process(target=run_command_on_host, args=(net.net.get('h4'), commands2[3]))
    process4.start()
    processes.append(process4)

    for process in processes :
        process.join()
    
    # Turn off the Mininet
    net.stopNetwork()

if __name__ == '__main__':
    main()
