"""
Mininet topology for IGMP snooping demo.
3 hosts, 1 OVS switch, remote POX controller.
Writes host PIDs to /tmp/igmp_demo_pids for tmux pane attachment.

Usage:
  sudo python3 ext/topo_igmp_demo.py
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


def run():
    setLogLevel('info')

    net = Mininet(switch=OVSSwitch, controller=RemoteController)

    net.addController('c0', ip='127.0.0.1', port=6633)
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    net.start()

    for host in [h1, h2, h3]:
        host.cmd('route add -net 224.0.0.0 netmask 240.0.0.0 dev %s-eth0' % host.name)
        host.cmd('sysctl -w net.ipv4.conf.%s-eth0.force_igmp_version=2' % host.name)

    with open('/tmp/igmp_demo_pids', 'w') as f:
        f.write(f"{net['h2'].pid}\n{net['h3'].pid}\n")

    print("\n=== IGMP Demo Topology Ready ===")
    print("h1 = multicast sender   (use Mininet CLI below)")
    print("h2 = subscriber         (bottom-left pane)")
    print("h3 = non-subscriber     (bottom-right pane)")
    print()
    print("CLI:  h2 iperf -s -u -B 224.1.1.1 -i 1 &")
    print("CLI:  h2 tcpdump -i h2-eth0 udp and dst 224.1.1.1 -v &")
    print("CLI:  h3 tcpdump -i h3-eth0 udp and dst 224.1.1.1 -v &")
    print("CLI:  h1 iperf -c 224.1.1.1 -u --ttl 5 -t 10")
    print("CLI:  h2 kill %2")
    print("CLI:  h3 kill %1")
    print()

    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()
