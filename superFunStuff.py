
#!/usr/bin/python

"""
To run it in mininet.
"""

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.util import pmonitor

def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=5))
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    p1 = h1.popen('python fun_probe.py --host %s --port %s' % (h1.IP(), '9030'))
    p2 = h2.popen('python fun_probe.py --host %s --port %s' % (h2.IP(), '9031'))
    p3 = h3.popen('python fun_collector.py --host %s --devicehosts %s ' % (h3.IP(), [h1.IP(), h2.IP()]))

    popens = { h1:p1, h2:p2, h3:p3 }
    for h, line in popens:
        print h + " " + line
    for h, line in pmonitor(popens):
        print "Monitoring output..."
        if h:
            print '%s: %s' % (h.name, line)
    CLI( net )

if __name__ == '__main__':
    main()