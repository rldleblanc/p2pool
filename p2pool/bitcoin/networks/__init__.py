import pkgutil
from importlib import import_module

nets = dict((name, import_module('p2pool.bitcoin.networks.%s' %name))
    for module_loader, name, ispkg in pkgutil.iter_modules(__path__))
for net_name, net in nets.items():
    net.NAME = net_name
