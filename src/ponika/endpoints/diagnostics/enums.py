from enum import Enum


class DiagnosticsIpProtocol(str, Enum):
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
